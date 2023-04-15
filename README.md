<!-- PROJECT LOGO -->
<!-- Thanks to https://github.com/othneildrew/Best-README-Template/blob/master/README.md-->
![Open Issues](https://img.shields.io/github/issues/nfoert/jadelauncher) 


<br />
<div align="center">
  
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="assets/JadeLauncherLogo.png", width=255>
    <source media="(prefers-color-scheme: dark)" srcset="assets/lightJadeLogo.png", width=255>
    <img alt="Jade Launcher">
  </picture>

  <h3 align="center">Jade Launcher</h3>

  <p align="center">
    The launcher for Jade Assistant or Jade Apps
    <br />
    <a href="https://nfoert.pythonanywhere.com/jadesite/jadelauncher"><strong>Download »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nfoert/jadelauncher/issues">Report Bugs »</a>
    ·
    <a href="https://nfoert.pythonanywhere.com/jadesite/contact">Contact me »</a>
  </p>
  <hr>
</div>

The Jade Launcher is the one and only place to manage your Jade Account and to download and launch apps like [Jade Assistant](https://github.com/nfoert/jadeassistant).

You can download the Jade Launcher [here](https://nfoert.pythonanywhere.com/jadesite/jadelauncher).

Sounds from [Notification Sounds](https://notificationsounds.com/)

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,github,vscode,qt" />
  </a>
</p>



## Building from source
Clone this repo using `git clone https://github.com/nfoert/jadelauncher`. Create a new virtual enviroment with `python -m venv .venv`. Activate it using the method for your system. Run `pip install -r requirements.txt` to install the necessary packages. Once that is done, also install `pyinstaller` with `pip install pyinstaller`. Finally, check that line 57 of `newJadeLauncher.py` has `developmental = False`. Then run `pyinstaller newJadeLauncherWINDOWS.spec` you should get a executable of the Jade Launcher inside the `dist` folder.
