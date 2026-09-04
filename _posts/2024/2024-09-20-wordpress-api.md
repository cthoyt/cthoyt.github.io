---
layout: post
title: Programmatic Access to a Wordpress User List
date: 2024-09-20 12:31:00 +0200
author: Charles Tapley Hoyt
tags:
  - Wordpress
  - Python
  - PHP
---

The [International Society of Biocuration (ISB)](https://www.biocuration.org/)
partners with the journal [Database](https://academic.oup.com/database) to get
discounts for its members when they publish there. This means the ISB's
executive committee needs to send a member list to the journal's editor.
Historically, this has been done manually by exporting the list from the
membership management plugin in the ISB Wordpress blog once per month and
emailing it to th This post is about my journey trying to automate it

# 1. There must be an API for this

Wordpress has a [programmatic API](https://developer.wordpress.org/rest-api/),
and specifically an endpoint to list
[users](https://developer.wordpress.org/rest-api/reference/users/).

After logging into the ISB's Wordpress site, I was able to list users by
navigating to the endpoint in browser
https://biocuration.org/wp-json/wp/v2/users. Note: this page won't work for you
unless you're on the EC and have admin powers. I wanted to replicate accessing
this page through a Python script, so I was suggested by the
[official Wordpress documentation](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/)
to create an application password and then use simple HTTP authentication. The
docs said try this, after replacing the username with the Wordpress account (for
me, that's `cthoyt`) and the application password, which is a string with the
form of `XXXX XXXX XXXX XXXX XXXX XXXX`. The documentation suggested doing the
following curl command, which works:

```shell
curl --user "USERNAME:PASSWORD" https://biocuration.org/wp-json/wp/v2/users
```

If you want to translate this to Python, it looks like this.

```python
import pystow, base64, requests

username = pystow.get_config("isb", "wordpress_username", raise_on_missing=True)
password = pystow.get_config("isb", "wordpress_password", raise_on_missing=True)

token = base64.b64encode(f"{username}:{password}".encode()).decode("utf-8")

res = requests.get(
    'https://www.biocuration.org/wp-json/wp/v2/users',
    headers={"Authorization": f"Basic {token}", "user-agent": "curl"},
)
```

Luckily, encoding the username/password string with basic authorization is such
a common pattern that the `request` (and any other modern library) has a nice
par for this.

```python
import pystow, requests

username = pystow.get_config("isb", "wordpress_username", raise_on_missing=True)
password = pystow.get_config("isb", "wordpress_password", raise_on_missing=True)

res = requests.get(
    'https://www.biocuration.org/wp-json/wp/v2/users',
    auth=(username, password),
    headers={"user-agent": "curl"}
)
```

I burned a ton of time with this because it turns out that Wordpress blocks both
the user agents for the `request` and `httpx` libraries. Therefore, you have to
explicitly set the `user-agent` header to something else, or you get a HTTP 403
forbidden error.

# 2. The API doesn't do what I wanted

It turns out that by default, all the users that never made a post get filtered
out. This is bad since the only users who are making posts on the ISB are the
handful who have or are currently on the executive committee.

So, obviously, the next step is to start injecting in PHP code to change how the
API works. I found a
[comment](https://github.com/WP-API/WP-API/issues/2300#issuecomment-299202391)
from Tim Jensen, a Wordpress developer, that suggests adding the following hooks
into the Wordpress theme's `functions.php` file by navigating to
https://www.biocuration.org/wp-admin/theme-editor.php?file=functions.php&theme=executive:

```php
function remove_has_published_posts_from_api_user_query($prepared_args, $request)
{
    unset($prepared_args['has_published_posts']);
    return $prepared_args;
}
add_filter('rest_user_query', 'remove_has_published_posts_from_api_user_query', 10, 2);
```

This actually worked! But, it wasn't the end of the story.

# 3. Full names are part of the plugin's metadata

It turns out that the user data model isn't all that comprehensive in Wordpress.
What we really needed was the full name and email address for each person, and
that was stored in an auxillary SQL table created and managed by the memberships
plugin. Note that the plugin lives on top of Wordpress's first-party users list,
and doesn't modify the API access to the user list.

So obviously, the next step was to add new API endpoints. I learned PHP at the
ripe age of 14 and when I learned some other languages, I never looked back, so
this wasn't so easy. Plus, Wordpress has a huge set of functions and idioms on
top. With a little help from ChatGPT, I was able to write a new API endpoint to
add to `functions.php` that got users whose membership expiration date is in the
future and joined in the metadata for their first and last names:

```php
function export_pmp_members_to_csv() {
    global $wpdb;

    // Set headers to make the response downloadable as a CSV file
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="members_export.csv";');
    header('Pragma: no-cache');
    header('Expires: 0');

    // Open output stream (in-memory file)
    $output = fopen('php://output', 'w');

    if (!$output) {
        return new WP_Error('file_error', 'Unable to generate CSV file.');
    }

    // Add CSV header row
    fputcsv($output, ['id', 'first', 'last', 'email', 'level', 'start', 'ends']);

    // Query to get PMP members and their membership details
    $results = $wpdb->get_results("
        SELECT
            u.ID,
            um_first_name.meta_value AS first_name,
            um_last_name.meta_value AS last_name,
            u.user_email, ml.name as membership_name,
            mu.startdate,
            mu.enddate
        FROM {$wpdb->users} u
        LEFT JOIN {$wpdb->prefix}pmpro_memberships_users mu ON u.ID = mu.user_id
        LEFT JOIN {$wpdb->prefix}pmpro_membership_levels ml ON mu.membership_id = ml.id
        LEFT JOIN {$wpdb->prefix}usermeta um_first_name ON u.ID = um_first_name.user_id
            AND um_first_name.meta_key = 'first_name'
        LEFT JOIN {$wpdb->prefix}usermeta um_last_name ON u.ID = um_last_name.user_id
            AND um_last_name.meta_key = 'last_name'
        WHERE mu.membership_id IS NOT NULL
            AND (mu.enddate > CURDATE() OR mu.enddate IS NULL)
    ");

    // Loop through results and write each row to the CSV
    foreach ($results as $row) {
        fputcsv($output, [
            $row->ID,
            $row->first_name,
            $row->last_name,
            $row->user_email,
            $row->membership_name,
            $row->startdate,
            $row->enddate
        ]);
    }

    // Close the output stream
    fclose($output);

    // Terminate script to ensure no extra output is sent
    exit;
}

function register_pmp_export_route() {
    // the actual path to the endpoint isn't important here
    register_rest_route('path/to/endpoint/', '/export-members', [
        'methods' => 'GET',
        'callback' => 'export_pmp_members_to_csv'
        'permission_callback' => function() {
            // Optionally, restrict access to logged-in users with specific capabilities
            return current_user_can('manage_options'); // Restrict to admin users
        }
    ]);
}
add_action('rest_api_init', 'register_pmp_export_route');
```

# 4. Automate it

Why stop at just being able to export the sheet? I wanted to go another mile and
make sure that Wordpress sends an email to the right person at the journal on a
monthly basis.

```php
/ Function to generate and send the CSV via email
function send_pmp_members_csv_via_email() {
    global $wpdb;

    // Create a temporary file to store the CSV
    $tmp_file = tempnam(sys_get_temp_dir(), 'pmp_csv_') . '.csv';
    $output = fopen($tmp_file, 'w');

    if (!$output) {
        return; // Handle error appropriately
    }

    // Add CSV header row
    fputcsv($output, ['ID', 'Username', 'First Name', 'Last Name', 'Email', 'Membership Level Name', 'Joined Date', 'Expires Date']);

    // Query to get PMP members and their membership details
    $results = $wpdb->get_results("
        SELECT u.ID,
            u.user_login,
            um_first_name.meta_value AS first_name,
            um_last_name.meta_value AS last_name,
            u.user_email,
            ml.name as membership_name
            mu.startdate,
            mu.enddate,
        FROM {$wpdb->users} u
        LEFT JOIN {$wpdb->prefix}pmpro_memberships_users mu ON u.ID = mu.user_id
        LEFT JOIN {$wpdb->prefix}pmpro_membership_levels ml ON mu.membership_id = ml.id
        LEFT JOIN {$wpdb->prefix}usermeta um_first_name ON u.ID = um_first_name.user_id
            AND um_first_name.meta_key = 'first_name'
        LEFT JOIN {$wpdb->prefix}usermeta um_last_name ON u.ID = um_last_name.user_id
            AND um_last_name.meta_key = 'last_name'
        WHERE mu.membership_id IS NOT NULL
        AND (mu.enddate > CURDATE() OR mu.enddate IS NULL)
    ");

    // Write data to CSV
    foreach ($results as $row) {
        fputcsv($output, [
            $row->ID,
            $row->user_login,
            $row->first_name,
            $row->last_name,
            $row->user_email,
            $row->membership_name,
            $row->startdate,
            $row->enddate
        ]);
    }

    // Close the file
    fclose($output);

    // Prepare email
    $to = ''; // Replace with recipient email
    $subject = 'ISB Monthly Members Report';
    $message = 'Please find the attached CSV file containing the list of active members of the International Society of Biocuration as of today.';
    $headers = array('Content-Type: text/csv; charset=UTF-8');

    // Send email with attachment
    wp_mail($to, $subject, $message, $headers, $tmp_file);

    // Clean up temporary file
    unlink($tmp_file);
}

// Schedule the cron job to run monthly
function schedule_monthly_csv_email() {
    if (!wp_next_scheduled('monthly_pmp_csv_email')) {
        wp_schedule_event(time(), 'monthly', 'monthly_pmp_csv_email');
    }
}
add_action('wp', 'schedule_monthly_csv_email');

// Hook the function to the cron event
add_action('monthly_pmp_csv_email', 'send_pmp_members_csv_via_email');
```

Hopefully I don't have to write anymore PHP for a long time :)
