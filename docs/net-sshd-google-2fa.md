## Installing the Google Authenticator PAM module
```bash
sudo apt install libpam-google-authenticator
```

## Generate TOTP seed
```bash
google-authenticator
```

It will ask you a series of questions, here is a recommended configuration:
- Make tokens “time-base””: yes
- Update the .google_authenticator file: yes
- Disallow multiple uses: yes
- Increase the original generation time limit: no
- Enable rate-limiting: yes

## Configure /etc/pam.d/sshd
To make SSH use the Google Authenticator PAM module, add the following line to the bottom of the **/etc/pam.d/sshd** file:
```bash
auth required pam_google_authenticator.so nullok
auth required pam_permit.so
```
- **nullok**: Allow users who have not configured 2fa to login using their preferred method, remove the nullok from the line to make 2FA mandatory.
- auth required pam_permit.so: support user login using their preferred method
If 

Edit line (usually at the top)
```bash
# Standard Un*x authentication.
#@include common-auth # Comment out this line
```
This will make pam ask for verification code instead of unix password (common-auth)

## Configure SSHD
```bash
# Add this entry or edit it if it is already existing
PermitRootLogin no

# We can explicitly set this although it should be the default value even if omitted. 
PubkeyAuthentication yes

# This setting will disable the password based authentication. 
PasswordAuthentication no

# This entry will allow both publickey authentication and keyboard-interactive which # we need to enter our TOTP code
AuthenticationMethods publickey,keyboard-interactive:pam

# PAM (Pluggable Authentication Modules) is also required to allow google 
# authenticator #integration
UsePAM yes

# Depending on your Debian version, if you find the entry 
# KbdInteractiveAuthentication existing in the config file, then use it, otherwise you 
# might find the deprecated entry which is ChallengeResponseAuthentication which
# in that case should be set to yes instead.
KbdInteractiveAuthentication yes
```

## Extra: bypass 2fa for local and/or IP addresses
```bash
Match address 192.168.1.1
    PasswordAuthentication yes
    AuthenticationMethods publickey password
    PermitRootLogin prohibit-password

Match address 192.168.0.0/24
    PasswordAuthentication yes
    AuthenticationMethods publickey password
    PermitRootLogin yes
```
Edit /etc/pam.d/sshd, Add line inb4 pam_google_authenticator.so
```bash
auth [success=1 default=ignore] pam_access.so accessfile=/etc/security/access-local.conf
auth required pam_google_authenticator.so
auth required pam_permit.so
```
Create /etc/security/access-local.conf file with the following content, also see **Caution**.
```bash
#localhost doesn't need two step verification
+:ALL:192.168.1.0/24
+:ALL:192.168.0.0/24
+:ALL:LOCAL

#All other hosts need two step verification
-:ALL:ALL

```
**Caution**: the linebreak at the end is mandatory or may caused this error in the auth log and skip 2fa for unwanted addresses
```bash
pam_access(sshd:auth): /etc/security/access-local.conf: line 6: missing newline or line too long
```
## Restart SSHD to apply new settings
```bash
sudo systemctl restart sshd.service
```
