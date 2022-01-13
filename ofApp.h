#pragma once

#include "ofMain.h"
#include "ofxCsv.h"
#include "ofxJSON.h"
#include "DriveData.hpp"

class ofApp : public ofBaseApp{

	public:
    void setup();
    void update();
    void draw();

    void keyPressed(int key);
    void keyReleased(int key);
    void mouseMoved(int x, int y );
    void mouseDragged(int x, int y, int button);
    void mousePressed(int x, int y, int button);
    void mouseReleased(int x, int y, int button);
    void mouseEntered(int x, int y);
    void mouseExited(int x, int y);
    void windowResized(int w, int h);
    void dragEvent(ofDragInfo dragInfo);
    void gotMessage(ofMessage msg);
    
    void drawDateString();
    
    int second;
    float fsecond;
    float dsec;
    bool ticked;
    
    int start_sec;
    int end_sec;
    
    float updatePerFrame;
    
    string readPath;
    ofImage map_streets;
    ofImage map_labels;
    ofxJSONElement json;
    
    vector<DriveData> drives;
    vector<DriveData *> existingDrives;
    map<int, vector<DriveData *>> time_drives_map;
    
    ofTrueTypeFont hv1;
    ofTrueTypeFont hv2;
};
