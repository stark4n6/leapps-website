---
title: Installing LEAPPs and LAVA on macOS with Homebrew
date: 2026-06-28
author: James Habben
tags: [LEAPPs, LAVA, macOS, Homebrew, installation]
excerpt: Mac users can install iLEAPP, ALEAPP, RLEAPP, VLEAPP, their GUI apps, and LAVA with a few Homebrew commands from the LEAPPs tap.
---

# Installing LEAPPs and LAVA on macOS with Homebrew

If you use a Mac for forensic work, you probably already have a small pile of tools installed through Homebrew. It is one of those quiet utilities that makes a workstation feel civilized: install the thing, update the thing, move on with your day.

The LEAPPs tools now fit into that workflow too.

There is an official Homebrew tap for the project at [leapps-org/homebrew-leapps](https://github.com/leapps-org/homebrew-leapps). Once the tap is added, macOS users can install the LEAPPs command line tools, the GUI apps, and LAVA with normal `brew` commands.

One quick reality check before the commands: a lot of forensic workstations are intentionally kept offline. Homebrew is happiest on a machine that can reach the internet. If your lab machine is air-gapped, this may not be all that helpful, but maybe you have a research system or a connected staging machine that can benefit from this.

## Add the tap

First, add the LEAPPs tap:

```bash
brew tap leapps-org/leapps
```

You only need to do this once. Homebrew will remember the tap until you remove it.

## Install the command line tools

If you like running parsers from the terminal, install whichever tools you need:

```bash
brew install ileapp
brew install aleapp
brew install rleapp
brew install vleapp
```

That gives you the command line versions of:

- `ileapp` for iOS
- `aleapp` for Android
- `rleapp` for warrant returns
- `vleapp` for vehicle systems

## Install the GUI apps

If you prefer the desktop apps, those are available as casks:

```bash
brew install --cask ileapp-gui
brew install --cask aleapp-gui
brew install --cask rleapp-gui
brew install --cask vleapp-gui
```

And for reviewing LEAPPs output in LAVA:

```bash
brew install --cask lava
```

That is the part I am happiest about. LAVA has become a really comfortable way to review LEAPPs output, especially when you are filtering tables, previewing media, or bouncing around a report during research. Being able to install it with a single Homebrew command feels right.

## Keeping everything updated

Homebrew handles updates in the usual way:

```bash
brew update
brew outdated
brew upgrade
```

If you only want to update specific LEAPPs tools, name them:

```bash
brew upgrade ileapp aleapp
```

For casks, Homebrew will also handle upgrades through the normal upgrade flow.

One more quick note: the Homebrew packages track *packaged releases*. They are not meant to follow every development commit between releases. If you need the newest parser work from a development branch, cloning the repo directly is still the way to do that.

## Removing tools

If you need to uninstall a command line tool:

```bash
brew uninstall ileapp
```

For GUI apps:

```bash
brew uninstall --cask ileapp-gui aleapp-gui vleapp-gui rleapp-gui lava
```

And if you ever want to remove the tap itself:

```bash
brew untap leapps-org/leapps
```

Untapping does not remove tools you already installed. It only removes the tap from Homebrew.

## A small quality-of-life win

This is not the flashiest project update, but it is one of those things that makes the tools easier to live with. New machine? Fresh lab Mac? Quick test system? Add the tap, install what you need, and get back to the actual forensic work.

That is a good kind of boring.
