#include "ofMain.h"
#include "ofApp.h"

glm::vec2 DriveData::coodToXY(float w, float h, glm::vec2 cood){
    return glm::vec2(cood.x * w, (1 - cood.y) * h);
}

ofColor DriveData::taxiYellow = ofColor(253,184,19);
ofColor DriveData::taxiYellowSub = ofColor::fromHex(0xff073a);

//========================================================================
int main( ){
	ofSetupOpenGL(1080,1080,OF_WINDOW); //1:1 window
//    ofSetupOpenGL(1440,1080,OF_WINDOW); //4:3 window
    

	// this kicks off the running of my app
	// can be OF_WINDOW or OF_FULLSCREEN
	// pass in width and height too:
	ofRunApp(new ofApp());

}
