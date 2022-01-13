#pragma once
#include <ofMain.h>
#include <ofxJSON.h>

class DriveData{
public:
    DriveData(Json::Value);
    void update();
    void displayRoute();
    bool isFinished();
    glm::vec2 culcCurrentPos();
    
    int passengers;
    string startLocation;
    string distinationLocation;
    
    glm::vec2 puPos;
    vector<glm::vec2> waypoints;
    vector<float> distances;
    glm::vec2 doPos;
    
    int pu_do_sec[2];
    
    float life;
    float dlife;
    
    float heading;
    
    int _tickcount = 0;
    
    static ofColor taxiYellow;
    static ofColor taxiYellowSub;
    
private:
    static glm::vec2 coodToXY(float w, float h, glm::vec2 cood);

};
