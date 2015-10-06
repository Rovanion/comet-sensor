Comet Web Sensor Data Handler
=============================

A dog simple script for retreiving and dealing with climate data from the Comet T6540 Climate sensor written in Python 3.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Comet Web Sensor Data Handler](#comet-web-sensor-data-handler)
    - [Dependencies](#dependencies)
    - [Usage](#usage)

<!-- markdown-toc end -->


Dependencies
------------

This project depends on the python module called click. On Debian and Ubuntu it's installed by running:

```bash
sudo apt-get install python3-click
```

On all Linux distributions it can be installed through pip, though it's always recommended to use the distribution package manager since those usually come with the promise of semi-automatic security updates.

```bash
pip install click
```

Usage
-----

In order to fetch sensor data from your Comet web sensor run the following:

```bash
comet fetch http://url.to.web.sensor
```

Since at least the T6540 only keeps 1000 data points you should do this at least 1000/samples\_per\_day times a day. Sample rate can be found in the general settings for your web sensor.

Example: The sample rate is once every minute. We should then fetch at least every 0.7 day or once every 16th hour.

But since the sensor clears its memory on reboot it's always safer to fetch more frequently.
