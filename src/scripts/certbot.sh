#!/bin/sh

install_certbot()
{
    sudo snap install core; sudo snap refresh core
    sudo apt-get remove certbot
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot    
}


issue_cert()
{
    sudo certbot certonly --nginx
}


renew_cert()
{
    sudo certbot renew --dry-run
}

