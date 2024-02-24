#!/bin/bash

read -rp "bot token: " bot_token
read -rp "admin id: " admin_id
read -rp "order notification id: " order_notification_id

read -rp "email from: " email_from
read -rp "email_from_password: " email_from_password
read -rp "email_to: " email_to


env_file="app/.env"

cat <<EOF >$env_file
# TELEGRAM
BOT_TOKEN=$bot_token
ADMIN_ID=$admin_id
ORDER_NOTIFICATION_ID=$order_notification_id

# EMAIL NOTIFICATIONS
EMAIL_FROM=$email_from
EMAIL_FROM_PASSWORD=$email_from_password
EMAIL_TO=$email_to
EOF
