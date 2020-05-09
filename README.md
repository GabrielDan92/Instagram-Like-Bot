# Instagram Like Bot

This is a fun project that I did on my own after building the script initially in VBA (yes, VBA). This is not a project I want to monetize (although there are several websites that charge money for using similar bots) and you should definitely follow Instagram's Terms of Use regarding using automated software on their platform. Use at your own risk.

This script creates an incognito Chrome instance, goes to Instagram's login page and populates the login details - that are not hardcoded in the python code - but rather retrieved from a json file (I've added in the repository the json template I'm using). The next step is reading the hashtag list provided and navigating to each hashtag homepage, and liking the pictures until a threshold is reached. 

A nice feature I've added after encountering an issue 'in production' was to first of all check the HTML attribute of Instagram's heart button, in order to find out if the image was already liked or not. Without this verification step, the script simply 'clicks' on the heart button and if that image was previously liked you simply take the like back, which is the opposite of the objective I have in mind. There is also an error handler in place: if for whatever reason the image is not loaded, the script closes the browser and goes to the next iteration, waiting for 10 minutes before starting the next session.

After a lot of trial and error (and account being restricted for several hours), the current formula that works for me in order to prevent being blocked/banned is liking 50 pictures for each hashtag with 2-3 seconds random delay between each action (the delay is being randomized in order to bypass whatever pattern check Instagram might have in place) and 10 minutes delay between each hashtag. After each iteration the Chrome instance is terminated and a new one is generate. This formula should and most probably will have to be changed depending on what Instagram is doing on their end to prevent automated bots from accessing their platform. </br>

</br>
![Script Demo](Media1.gif)
