# Epic Seven Auto Gearscore Calculator (e7-agc)

An automatic gearscore calculator for the mobile game [Epic Seven](https://epic7.smilegatemegaport.com/#home)

## Description

The automatic gearscore calculator uses the open source [tesseract](https://github.com/tesseract-ocr/tesseract) OCR to read in gear information, such as the picture below, from the mobile game [Epic Seven](https://epic7.smilegatemegaport.com/#home). Data is then parsed and gear score is then calculated based on its maximum potential and displayed.

![Example gear](.//images/Epic%20Seven%20example%20gear.PNG)

## How it works

1. Grab a screenshot of the game window
2. Checks if top left corner is either 'Enhance Equipment' or 'Substat Modification' using pytesseract, if true set state to true, otherwise state is false
3. When state changes from false to true, trigger main logic
4. Using cv2, crop and preprocess the screenshot to get relevant gear information and pass to pytesseract
5. Parse output from pytesseract and pass to gear calculation
6. Repeat from step 1

Gear with bounding boxes:
![Gear with bounding boxes](.//images/Gear%20with%20bounding%20boxes.PNG)

Processed substat names and values to pass to pytesseract:
![Processed substats](.//images/Processed%20substat%20images.PNG)

## Getting Started (WIP)

### Dependencies

<!-- - Describe any prerequisites, libraries, OS version, etc., needed before installing program.
- ex. Windows 10 -->

### Installing

<!-- - How/where to download your program
- Any modifications needed to be made to files/folders -->

### Executing program

<!-- - How to run the program
- Step-by-step bullets

```
code blocks for commands
``` -->

## Help (WIP)

<!--- Any advise for common problems or issues. --->

## Version History (WIP)

<!-- - 0.2
  - Various bug fixes and optimizations
  - See [commit change]() or See [release history]()
- 0.1
  - Initial Release -->

<!-- ## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details -->

## Acknowledgments (WIP)

<!-- Inspiration, code snippets, etc.

- [awesome-readme](https://github.com/matiassingers/awesome-readme)
- [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
- [dbader](https://github.com/dbader/readme-template)
- [zenorocha](https://gist.github.com/zenorocha/4526327)
- [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46) -->
