# fragment
Python Flask project used to aggregate and distribute IRC meeting minutes and logs for the Fedora Project

## Note

The repository has been archived and the code has been moved away to https://github.com/fedora-infra/mote/tree/fragment.

## How to set up?

1. Download https://drive.google.com/file/d/1iOKEgyHMtpnCwsuZa5ufT8gI9-ntuOVc/view?usp=sharing.
2. Extract the contents to `/srv/web/meetbot` directory. 
3. `git clone https://github.com/t0xic0der/fragment.git`
4. `cd fragment/`
5. `virtualenv venv`
6. `source venv/bin/activate`
7. `pip3 install -r requirements.txt`
8. `python3 main.py --help`
9. `python3 main.py -p 9696 -4`

Detailed documentation would arrive shortly. Inconvenience is regretted.
