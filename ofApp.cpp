#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
    ofSetVerticalSync(true);
    ofSetFrameRate(60);
    ofBackground(0, 0, 0);
    
    //各種ファイルをロード
    readPath = "../../../files/1/";
    map_streets.load(readPath + "map1.png");
    map_labels.load(readPath + "map2.png");
    json.open(readPath + "datas.json");
    
    //タクシーの運行データの保存(出発時間，出発地点，目的地，所要時間など)
    drives.clear();
    for(int i=0; i<json.size(); i++){
        DriveData thisrow(json[i]);
        drives.push_back(thisrow);
    }
    
    //データの存在した現実時間の範囲を取得
    //あわせて，Map<出発時間 -> 運行データ>のマップを作成
    start_sec = INT_MAX;
    end_sec = 0;
    
    //秒数，少数単位
    fsecond = 0.0;
    //更新あたりの経過秒数，最低時間単位
    dsec = 1.0/10;
    //1フレームあたりの更新回数
    updatePerFrame = 5;
    
    for(int i=0; i<drives.size(); i++){
        int pu_sec = drives[i].pu_do_sec[0];
        int do_sec = drives[i].pu_do_sec[1];
        
        if(pu_sec < start_sec){
            start_sec = pu_sec;
        }
        if(pu_sec > end_sec){
            end_sec = pu_sec;
        }
        
        int duration = do_sec - pu_sec;
        
        drives[i].life = 1.0;
        drives[i].dlife = dsec / duration;
        
        time_drives_map[pu_sec].push_back(&(drives[i]));
    }
    
    second = start_sec;
    
    hv1.load("Helvetica_01.ttf", 12);
    hv2.load("Helvetica_01.ttf", 56);

}

//--------------------------------------------------------------
void ofApp::update(){
    //コード内の時間を更新．
    //秒数(整数)が更新されたら，表示するデータにその時間出発のデータを追加する．
    //あわせて，目的地に到着したデータを削除
    for(int _=0; _<updatePerFrame; _++){
        
        if(int(fsecond+dsec) != int(fsecond)){
            second += 1;
            
            vector<DriveData* > newDrives = time_drives_map[second];
            existingDrives.insert(existingDrives.end(), newDrives.begin(), newDrives.end());
        }
        
        fsecond += dsec;
        
        ofRemove(existingDrives, [](DriveData* n){ return n->isFinished(); });
        
        for(DriveData* ptrData: existingDrives){
            ptrData->update();
        }
    }
    
}

//--------------------------------------------------------------
void ofApp::draw(){
    
    ofSetColor(60);
    map_streets.draw(0, 0, ofGetWidth(), ofGetHeight());
    
    for(DriveData* ptrData: existingDrives){
        ptrData->displayRoute();
    }
    
    ofSetColor(255, 255, 255);
    map_labels.draw(0, 0, ofGetWidth(), ofGetHeight());
    
    ofSetColor(0, 0, 0);
    ofFill();
    ofDrawRectangle(0, ofGetHeight()-30, ofGetWidth(), 30);
    drawDateString();
    
    //ofSaveScreen("frames/"+ofToString(ofGetFrameNum()) + ".png");
}

//--------------------------------------------------------------
void ofApp::drawDateString(){
    
    time_t now = second - 46800;
    struct tm *ts;
    char buf[80];
    
    ts = localtime(&now);
    strftime(buf, sizeof(buf), "%Y/%m/%d%H:%M:%S", ts);
    
    string datetime(buf);
    
    string date = datetime.substr(0, 10);
    string time = datetime.substr(10, 18);
    
    ofSetColor(255);
    ofFill();
    
    float w=ofGetWidth(), h=ofGetHeight();
    hv1.drawString(date, 10, h-5);
    hv1.drawString(time, 100, h-5);
    //hv2.drawString(time, 140, 180);
    
}


//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    if(key == 's'){
        ofSaveScreen("frame/"+ofToString(ofGetFrameNum()) + ".JPG");
    }

}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------w
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}
