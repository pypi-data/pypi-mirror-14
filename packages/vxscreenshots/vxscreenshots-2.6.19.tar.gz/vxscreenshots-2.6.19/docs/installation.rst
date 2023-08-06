.. highlight:: shell

============
Installation
============


On Ubuntu 14.04 and 15.04.
==========================

At the command line::

    $ sudo apt-get update && sudo apt-get -y install python-pip awscli shutter

Now install it from pip, isolated on your user (recommended).::

    $ pip install vxscreenshots --user && \
      echo "export PATH=\$PATH:$HOME/.local/bin" >> $HOME/.profile && \
      source $HOME/.profile

or with sudo.::

    $ sudo pip install vxscreenshots

Note::

    Due to we created some helpers scripts sudo is a good idea, but you can
    use the --user option as mentioned before if you want all isolated in your
    own user profile.

Now run 2 tools in order to create all configuration files.::

    $ vxssicon

    This should run normally ctrl+c to kill it.

    $ vxsswatcher

    This should run normally ctrl+c to kill it.

**Now we need to set Amazon S3 Credenetials**.
==============================================

Before make a first example we need to set amazon credentials as boto3
configuration `indicates`_. And set your parameters for bucket and local
directories to be watched.::

    $ aws configure
    AWS Access Key ID [None]: YOURKEY_ID
    AWS Secret Access Key [None]: YOURKEYASKEDTOAMAZON
    Default region name [None]: us-east-1
    Default output format [None]:  

**Configuring**

You will need to configure a little values.

1. First set the folder you want to supervise in the **supervised** entry on the
   configuration file.
2. Secondly The folder name would be your Linux user in order to have some kind
   of order but if you use this in several machines at once this it should be
   useful set it manually either, different per machine.
3. The bucket is the name of the bucket itself configuring with a proper DNS
   entry in order to set the link properly when sharing following amazon_ 
   standards.::

    $ gedit $HOME/.vxscreenshots/vxsscreenshots.ini

**Let's test what we have**
===========================

This program is composed by 2 daemons and one script.:

1. **vxsswatcher**: one which watch the folder configured with pictures and push 
    everything which is new/modified to s3, recording such information in the 
    cache database.
2. **vxssicon**: which gives a graphical interface to allow you get some 
    interesting links automatically into the clipboard and other features.
3. **screenshot.sh**: Script that runs your screenshot manager (shutter by 
    default) and save a file with an proper aleatory name on a watched folder.

Then open 2 bash consoles and run both again after you configured the amazon 
key, then run both daemons, you should see something like this.

.. image:: http://screenshots.vauxoo.com/oem/testing_vxscreenshots.png
    :width: 800px
    :alt: How desktop looks like
    :align: center


Install last version of shutter.
================================

Shutter is the most powerful screenshots manager in the Linux world, then we 
will manage our screenshots with it.

You can add a PPA to your system with a single line in your terminal. Open a 
terminal and enter::

    $ sudo add-apt-repository ppa:shutter/ppa

Now, as a one-off, you should tell your system to pull down the latest list of 
software from each archive it knows about, including the PPA you just added::

    $ sudo apt-get update

Install Shutter.::

    $ sudo apt-get install shutter

Configure all services.
=======================

Execute the configuration options.

    $ vxssicon --configure

This will add all services at start session in order to avoid start everything 
manually.

Configure Shutter shortcuts alá Skitch.
---------------------------------------

* Go to keyboard configuration.


.. image:: http://screenshots.vauxoo.com/oem/c8ebcf-403x318.png
   :width: 400
   :alt: alternate text


* Set the proper values to run shutter.

.. image:: http://screenshots.vauxoo.com/oem/81197c-931x552.png
   :width: 400
   :alt: alternate text

* Now you can go to the :doc:`usage` section to see how enjoy the features just
  configured and installed.

Now just restart the graphical sesion (logout and login) or simply restart your
PC yo see how all is working since the start.

.. _indicates: http://boto3.readthedocs.org/en/latest/guide/configuration.html#shared-credentials-file
.. _amazon: http://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html
.. _this: http://shutter-project.org/faq-help/set-shutter-as-the-default-screenshot-tool/

