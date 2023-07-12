import duo_client
from datetime import datetime, timedelta
import json
import config


# Duo API credentials
api = duo_client.Admin(
    ikey=config.IKEY,
    skey=config.SKEY,
    host=config.API_HOSTNAME
)
auth = duo_client.Auth(
    ikey=config.IKEY,
    skey=config.SKEY,
    host=config.API_HOSTNAME)

# Pull user list
for user in api.get_users():
    # Checks if user is enrolled
    enrollStatus = user['is_enrolled']
    if bool(enrollStatus) is False:
        # Checks if user is pending deletion to limit errors
        userStatus = user['status']
        if userStatus != 'pending deletion':
            # Checks if user is a service account
            userID = user['user_id']
            userEmail = user['email']
            if userID not in config.SERVICE_ACCOUNTS:
                # Users not enrolled are synced from Azure
                try:
                    api.sync_user(userEmail,config.DIRECTORY)
                    print(f"User '{user['username']}' synced from Azure to get Windows 10 Bypass groups.")
                except RuntimeError as e:
                    print(f'Error setting bypass: {e}')
    else:
        continue
