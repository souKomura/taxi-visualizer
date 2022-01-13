#include "DriveData.hpp"

DriveData::DriveData(Json::Value jsonvalues){
    passengers = jsonvalues["number_of_passanger"].asInt();
    startLocation = jsonvalues["locations"][0].asString();
    distinationLocation = jsonvalues["locations"][1].asString();
    
    //pickup / dropoff time
    puPos.x = jsonvalues["pickup_normalized"][0].asFloat();
    puPos.y = jsonvalues["pickup_normalized"][1].asFloat();
    doPos.x = jsonvalues["dropoff_normalized"][0].asFloat();
    doPos.y = jsonvalues["dropoff_normalized"][1].asFloat();
    
    for(int i=0; i<jsonvalues["waypoint_with_dist"].size(); i++){
        distances.push_back(jsonvalues["waypoint_with_dist"][i][0].asFloat());
        
        glm::vec2 waypoint;
        waypoint.x = jsonvalues["waypoint_with_dist"][i][1][0].asFloat();
        waypoint.y = jsonvalues["waypoint_with_dist"][i][1][1].asFloat();
        waypoints.push_back(waypoint);
    }
    
    pu_do_sec[0] = jsonvalues["time_range"][0].asInt();
    pu_do_sec[1] = jsonvalues["time_range"][1].asInt();
}

//--------------------------------------------------------------
void DriveData::update(){
    life -= dlife;
    _tickcount++;
}

//--------------------------------------------------------------
void DriveData::displayRoute(){

    //乗車数1人:黄色 いっぱい:赤
    ofSetColor(taxiYellowSub.getLerped(taxiYellow, sqrt(1.0/passengers)), 180);
    
    ofFill();
    glm::vec2 nowOn = culcCurrentPos();
    
    ofPushMatrix();
    ofTranslate(coodToXY(ofGetWidth(), ofGetHeight(), nowOn));
    
    
    ofRotateZRad(heading);
    ofSetLineWidth(1);
    ofDrawLine(nowOn.x, nowOn.y, 3, 0);
    //ofDrawRectaWngle(-1, -1, 3, 2);
//    ofDrawCircle(nowOn, 1);
    
    ofSetColor(taxiYellowSub.getLerped(taxiYellow, sqrt(1.0/passengers)), 1);
    ofDrawCircle(nowOn, 13);
    
    ofPopMatrix();
    
//    ofSetLineWidth(2);
//    ofNoFill();
//    ofBeginShape();
//    for(int i=0; i<waypoints.size(); i++){
//        ofVertex(coodToXY(ofGetWidth(), ofGetHeight(), waypoints[i]));
//    }
//    ofEndShape();
    
}

//--------------------------------------------------------------
glm::vec2 DriveData::culcCurrentPos(){
    /**
     *Compute current (estimated) position from ordered waypoints and this life.
     *When the life is 1 this is on departure. on the destination with life 1.
     */
    
    int i;
    float progress = 1.0 - life;
    float distsum = 0.0;
    
    for(i=0; i<distances.size(); i++){
        if(progress < distsum + distances[i]){
            break;
        }
        distsum += distances[i];
    }
    
    float section_progress = (progress - distsum) / distances[i];
    
    glm::vec2 prev = waypoints[i-1];
    glm::vec2 next = waypoints[i];
    
    heading = atan2(next.x - prev.x, next.y - prev.y) - PI/2;

    glm::vec2 result = (next * section_progress) + (prev * (1.0 - section_progress));
    
    return result;
}

//--------------------------------------------------------------
bool DriveData::isFinished(){
    return life < 0;
}
