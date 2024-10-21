==============
Android device
==============

Download app.apk file
=====================

* Download ``app.apk`` file to you mobile device to any folder.
* Click on ``app.apk`` file in folder your device.
  Will open install dialog.
* Click install.

Compile the android app.apk
===========================

Path to compiled app.apk::

    wse/build/wse/android/gradle/app/build/outputs/apk/debug/app-debug.apk

In development mode.

.. seealso::

   For detailed documentation and installation on **Windows**, see the official documentation website.

   `Official documentation <https://docs.beeware.org/en/latest/tutorial/tutorial-7.html#updating-dependencies>`_

You will need to make 2 changes to the options on your device:

 * Enable developer options
 * Enable USB debugging

Set on mobile device the development mode.

Connect mobile device to your computer with a USB cable.

**Run in console:**

.. code-block:: console

   briefcase create android

.. code-block:: console

   briefcase build android

.. code-block:: console

   briefcase run android

Select mobile device to install, install.

Possible problems install to devise
-----------------------------------

.. seealso::

   `Run the app on a physical device <https://docs.beeware.org/en/latest/tutorial/tutorial-5/android.html#run-the-app-on-a-physical-device>`_

Possible problems runs on devise
================================

The application starts on device and immediately closes
-------------------------------------------------------

**1. Problem:**

* The imported python library was not added to **pyproject.toml** during development.

**Solution:**

* Updating dependencies, see: `Official documentation <https://docs.beeware.org/en/latest/tutorial/tutorial-7.html#updating-dependencies>`_

**2. Problem:**

* The python-dotenv library was used in the development.

**Solution:**

* The correct solution to the problem is unknown.
