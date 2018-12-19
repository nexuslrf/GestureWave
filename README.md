You can use this project for your research. No commercial usage. 


### Gesture recognition using the soundwave doppler effect
Authors: 
- Manuel Dudda
- Benjamin Weißer
- Paul Pasler
- Sebastian Rieder
- Alexander Baumgärtner
- Robert Brylka
- Annalena Gutheil
- Matthias Volland
- Daniel Andrés López
- Frank Reichwein

Based on research at: http://research.microsoft.com/en-us/um/redmond/groups/cue/soundwave/

The application is used to sense gestures with soundwaves based on the Doppler Effect. Below is a list of defined gestures. 

Class number - Gesture Shortcode -  Gesture description

0 RLO 	Right-To-Left-One-Hand or Left-To-Right-One-hand
1 TBO 	Top-To-Bottom-One-Hand
2 OT 	Opposed-With-Two-hands
3 SPO 	Single-Push-One-Hand
4 DPO 	Double-Push-One-Hand
5 RO 	Rotate-One-Hand
6 BNS 	Background-Noise-Silent (no gesture, but in silent room)
7 BNN 	Background-Noise-Noisy (no gesture, but in a noisy room like a Pub, an office, a kitchen, etc.)


Features:
- Record training examples
	via GUI
	via integrated console and batch mode
- Use different classification methods
	Support Vector Machines
	Hidden Markov Models
	k-Means
	Decisiontrees, Boosting and Bagging
	Long Short Term Memory - Neronal Networks
- Train the classification methods with recoreded sample data
- Load and save trained classificators
- Live classification with one classificator
- Customizable via personal configuration file

Requirements:
- Microphone which can record sound from frequency 17500 Hz up to 19500 Hz
- Speakers which can produce a constant frequency at 18500 Hz
- a suitable microphone speaker configuration (examples are laptop based)
	Speaker left and right from keyboard, microphone below display
	Speaker left and right from keyboard, microphone above display

Installation:
see Install file

Usage:
	cd {ProjectFolder}/src
	python senseGesture.py
	type 'h' for print available commands
	- not all commands can be used by all classificators
	
example: 
	For recording 50 times the gesture 0 type:
	0 50 

### Usage of a classifier see in README_[classifier]

###Available commands (output of 'h u' command)
Usage: <command> [<option>]

Record example gestures
  r 			start/stop sound playing and recording
  <num> [<num>]	0-7 record a gesture and associate with class number [repeat <digit> times]
  f [<string>] 	change filename for recording. if empty use current time 

Gui [BUG: works only one time per runtime]
  g 		start view (can record single gestures)
  gg 		start bob view

Classifier commands
  u <classifier> 	configure classifier to use. Supported classifiers: [svm, trees, hmm, k-means, lstm]
  c 				start real time classifying with the configured classifier (requires active sound, see 'r' command)
  t [<num>] 		start training for the configured classifier with the saved data, <num> Number of epochs, if applicable
  l <filename> 		load configured classifier from file
  l ds <filename> 	load configured dataset from file
  s [<filename>] 	save configured classifier to file with filename or timestamp
  s ds [<filename>] save configured dataset to file with filename or timestamp
  v 				start validation for the configured classifier with the saved data
  p 				print the classifier options

General
  h 		print all help
  h u 		print usage help
  h g 		print gesture table
  e 		exit application

	
