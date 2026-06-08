### BEStamer v9 - Excel Export + All Features MQL4

//+------------------------------------------------------------------+
//| BEStamer v9 Ultimate.mq4 |
//| Excel Export.CSV + Full Materials + Auto/Manual Drawing |
//+------------------------------------------------------------------+
#property strict
#property indicator_chart_window

//--- MATERIALS ZOSE 20 + SUBTYPES
string MainMaterials[] = {
   "CEMENT","SAND","GRAVEL","STEEL_BAR","BRICKS",
   "TIMBER","IRON_SHEET","PAINT","TILES","NAILS",
   "CONCRETE","GLASS","PVC_PIPES","WIRES","BLOCKS",
   "WATERPROOF","CEILING","DOORS","WINDOWS","AGGREGATE"
};

string SubTypes_CEMENT[] = {"CEM I 42.5R","CEM II 32.5N","WHITE_CEMENT","QUICK_SET","PORTLAND"};
string SubTypes_SAND[] = {"RIVER_SAND","CRUSHED_SAND","PLASTER_SAND","FILLING_SAND"};
string SubTypes_GRAVEL[] = {"10MM","20MM","25MM","40MM","BALLAST"};
string SubTypes_STEEL_BAR[] = {"D8","D10","D12","D16","D20","D25","D32"};
string SubTypes_BRICKS[] = {"CLAY_BURNED","CEMENT_BLOCK","HOLLOW_BLOCK","PAVERS","FACE_BRICK"};
string SubTypes_TIMBER[] = {"HARDWOOD","SOFTWOOD","PLYWOOD","MDF","CYPRESS","PINE"};
string SubTypes_IRON_SHEET[] = {"VERSATILE","CORRUGATED","IT4","RESINCOT","GAUGE_28","GAUGE_30"};
string SubTypes_PAINT[] = {"WATER_BASED","OIL_BASED","WEATHER_GUARD","UNDERCOAT","VARNISH"};
string SubTypes_TILES[] = {"CERAMIC","PORCELAIN","GRANITE","MARBLE","PVC_TILE"};
string SubTypes_NAILS[] = {"1_INCH","2_INCH","3_INCH","4_INCH","ROOFING_NAIL","CONCRETE_NAIL"};
string SubTypes_CONCRETE[] = {"C15","C20","C25","C30","READY_MIX"};
string SubTypes_GLASS[] = {"4MM_CLEAR","5MM_TINTED","6MM_LAMINATED","MIRROR","FROSTED"};
string SubTypes_PVC_PIPES[] = {"1/2_INCH","3/4_INCH","1_INCH","2_INCH","4_INCH","WASTE_PIPE"};
string SubTypes_WIRES[] = {"1.5MM","2.5MM","4MM","6MM","10MM","TWIN_EARTH"};
string SubTypes_BLOCKS[] = {"SOLID_6","SOLID_9","HOLLOW_6","HOLLOW_9","VENT_BLOCK"};
string SubTypes_WATERPROOF[] = {"BITUMEN","APP","CEMENTITIOUS","LIQUID_MEMBRANE"};
string SubTypes_CEILING[] = {"GYPSUM","PVC","ACOUSTIC","WOODEN","SUSPENDED"};
string SubTypes_DOORS[] = {"FLUSH","PANEL","STEEL","GLASS_DOOR","PVC_DOOR"};
string SubTypes_WINDOWS[] = {"SLIDING","CASEMENT","LOUVER","ALUMINIUM","WOODEN"};
string SubTypes_AGGREGATE[] = {"DUST","CHIPS","COARSE","FINE","CRUSHED_STONE"};

//--- Settings
input string DrawingSettings = "===== DRAWING READER =====";
input bool ReadAutoDrawing = true;
input bool ReadManualDrawing = true;
input string AutoPrefix = "Auto_";

input string ExcelSettings = "===== EXCEL EXPORT =====";
input bool AutoExportExcel = true; // Yandike muri Excel buri break
input string FileName = "BEStamer_BOQ.csv"; // Izina rya file

input string QtySettings = "===== HIGH CAPACITY QTY =====";
input long MaxQuantity = 999999999;
input int DefaultQty = 100;

string SelectedMain = "";
string SelectedSub = "";
long SelectedQty = 0;
int SelectedMainIndex = -1;
int ExportCount = 0;

//+------------------------------------------------------------------+
int OnInit(){
   CreateMainPanel();
   CreateQtyPanel();
   CreateExcelButton();
   InitExcelFile(); // Kora file ya Excel niba idahari
   LoadSavedSelection();
   Print("BEStamer v9 Excel Ready. File: ",FileName);
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason){ SaveSelection(); ObjectsDeleteAll(0,"PANEL_"); ObjectsDeleteAll(0,"BTN_"); }

//+------------------------------------------------------------------+
void OnTick(){
   if(!IsNewCandle()) return;
   ReadAllDrawings();
   UpdateInfoPanel();
}

//+------------------------------------------------------------------+
void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam){
   if(id == CHARTEVENT_OBJECT_CLICK){
      // MAIN MATERIAL
      for(int i=0; i<ArraySize(MainMaterials); i++){
         if(sparam == "BTN_MAIN_"+MainMaterials[i]){
            SelectedMain = MainMaterials[i];
            SelectedMainIndex = i;
            SelectedSub = "";
            DeleteSubPanel();
            CreateSubPanel(i);
            HighlightMainButton(i);
            return;
         }
      }
      
      // SUB TYPE
      if(StringFind(sparam,"BTN_SUB_") >= 0){
         SelectedSub = StringSubstr(sparam,8);
         HighlightSubButton(sparam);
         ShowQtyPanel();
         return;
      }
      
      // QTY BUTTONS
      if(sparam=="BTN_QTY_ADD") ChangeQty(1);
      if(sparam=="BTN_QTY_SUB") ChangeQty(-1);
      if(sparam=="BTN_QTY_X10") ChangeQty(10);
      if(sparam=="BTN_QTY_X100") ChangeQty(100);
      if(sparam=="BTN_QTY_X1000") ChangeQty(1000);
      if(sparam=="BTN_QTY_SAVE") SaveCurrentSelection();
      
      // EXPORT BUTTON
      if(sparam=="BTN_EXPORT") ExportToExcelManual();
   }
   
   // EDIT QTY DIRECT
   if(id==CHARTEVENT_OBJECT_ENDEDIT && sparam=="EDIT_QTY"){
      string val = ObjectGetString(0,"EDIT_QTY",OBJPROP_TEXT);
      SelectedQty = StringToInteger(val);
      if(SelectedQty > MaxQuantity) SelectedQty = MaxQuantity;
      UpdateQtyDisplay();
   }
}

//+------------------------------------------------------------------+
// SOMA DRAWINGS + EXPORT TO EXCEL
void ReadAllDrawings(){
   int total = ObjectsTotal(0,0,-1);
   for(int i=total-1; i>=0; i--){
      string name = ObjectName(0,i);
      int type = ObjectType(name);
      if(type!=OBJ_TREND && type!=OBJ_HLINE && type!=OBJ_RECTANGLE) continue;
      
      bool isAuto = StringFind(name,AutoPrefix) >= 0;
      if(ReadManualDrawing &&!isAuto) ProcessDrawing(name,"MANUAL");
      if(ReadAutoDrawing && isAuto) ProcessDrawing(name,"AUTO");
   }
}

//+------------------------------------------------------------------+
void ProcessDrawing(string name, string mode){
   if(SelectedMain=="" || SelectedSub=="") return;
   if(SelectedQty<=0) return;
   
   static datetime lastAlert[];
   ArrayResize(lastAlert,1);
   
   // Irinde alert nyinshi kuri line imwe
   if(TimeCurrent() - lastAlert[0] < 60) return;
   
   double price = ObjectGetValueByShift(name,0);
   if(price==0) return;
   
   if(Bid > price){ // Drawing yacitswe
      lastAlert[0] = TimeCurrent();
      ExportCount++;
      
      if(AutoExportExcel) ExportToExcel(name, mode, price);
      
      string msg = mode+" BREAK: "+SelectedMain+"->"+SelectedSub+" QTY:"+IntegerToString(SelectedQty);
      Alert(msg);
      Print(msg," | Exported #",ExportCount);
   }
}

//+------------------------------------------------------------------+
// EXCEL EXPORT FUNCTIONS
void InitExcelFile(){
   if(!FileIsExist(FileName)){
      int handle = FileOpen(FileName, FILE_WRITE|FILE_CSV|FILE_ANSI);
      if(handle!=INVALID_HANDLE){
         // Header ya Excel
         FileWrite(handle,"Date","Time","Symbol","Drawing","Mode","Material","SubType","Quantity","Price","Scale_mm","Export_ID");
         FileClose(handle);
         Print("Excel file created: ",FileName);
      }
   }
}

void ExportToExcel(string dwgName, string mode, double price){
   int handle = FileOpen(FileName, FILE_READ|FILE_WRITE|FILE_CSV|FILE_ANSI);
   if(handle!=INVALID_HANDLE){
      FileSeek(handle,0,SEEK_END); // Jya ku mpera ya file
      
      string date = TimeToString(TimeCurrent(),TIME_DATE);
      string time = TimeToString(TimeCurrent(),TIME_MINUTES);
      
      FileWrite(handle,
         date,
         time,
         Symbol(),
         dwgName,
         mode,
         SelectedMain,
         SelectedSub,
         IntegerToString(SelectedQty),
         DoubleToString(price,Digits),
         DoubleToString(GetDrawingScaleMM(),0),
         IntegerToString(ExportCount)
      );
      FileClose(handle);
   }
}

void ExportToExcelManual(){
   if(SelectedMain=="" || SelectedSub==""){
      Alert("Banza uhitemo Material na SubType!");
      return;
   }
   ExportCount++;
   ExportToExcel("MANUAL_EXPORT","USER",Close[0]);
   Alert("Exported to Excel: "+SelectedMain+"->"+SelectedSub+" Qty:"+IntegerToString(SelectedQty));
}

//+------------------------------------------------------------------+
// UI FUNCTIONS
void CreateMainPanel(){
   int x=10,y=20,w=110,h=18,cols=4;
   int rows = MathCeil(ArraySize(MainMaterials)/(double)cols);
   
   ObjectCreate(0,"PANEL_BG_MAIN",OBJ_RECTANGLE_LABEL,0,0,0);
   ObjectSetInteger(0,"PANEL_BG_MAIN",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"PANEL_BG_MAIN",OBJPROP_XDISTANCE,x-5);
   ObjectSetInteger(0,"PANEL_BG_MAIN",OBJPROP_YDISTANCE,y-5);
   ObjectSetInteger(0,"PANEL_BG_MAIN",OBJPROP_XSIZE,w*cols+15);
   ObjectSetInteger(0,"PANEL_BG_MAIN",OBJPROP_YSIZE,rows*20+40);
   ObjectSetInteger(0,"PANEL_BG_MAIN",OBJPROP_BGCOLOR,C'20,20,20');
   
   ObjectCreate(0,"PANEL_TITLE_MAIN",OBJ_LABEL,0,0,0);
   ObjectSetString(0,"PANEL_TITLE_MAIN",OBJPROP_TEXT,"1. MATERIALS - ALL 20");
   ObjectSetInteger(0,"PANEL_TITLE_MAIN",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"PANEL_TITLE_MAIN",OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,"PANEL_TITLE_MAIN",OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,"PANEL_TITLE_MAIN",OBJPROP_COLOR,clrOrange);
   
   for(int i=0; i<ArraySize(MainMaterials); i++){
      int col = i % cols;
      int row = i / cols;
      string name = "BTN_MAIN_"+MainMaterials[i];
      ObjectCreate(0,name,OBJ_BUTTON,0,0,0);
      ObjectSetInteger(0,name,OBJPROP_CORNER,CORNER_LEFT_UPPER);
      ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x+col*(w+2));
      ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y+25+row*20);
      ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
      ObjectSetInteger(0,name,OBJPROP_YSIZE,h);
      ObjectSetString(0,name,OBJPROP_TEXT,MainMaterials[i]);
      ObjectSetInteger(0,name,OBJPROP_BGCOLOR,clrDarkGray);
      ObjectSetInteger(0,name,OBJPROP_COLOR,clrWhite);
      ObjectSetInteger(0,name,OBJPROP_FONTSIZE,7);
   }
}

void CreateSubPanel(int mainIndex){
   string subArray[]; GetSubTypes(mainIndex, subArray);
   int x=10,y=180,w=115,h=18,cols=4;
   int rows = MathCeil(ArraySize(subArray)/(double)cols);
   
   ObjectCreate(0,"PANEL_BG_SUB",OBJ_RECTANGLE_LABEL,0,0,0);
   ObjectSetInteger(0,"PANEL_BG_SUB",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"PANEL_BG_SUB",OBJPROP_XDISTANCE,x-5);
   ObjectSetInteger(0,"PANEL_BG_SUB",OBJPROP_YDISTANCE,y-5);
   ObjectSetInteger(0,"PANEL_BG_SUB",OBJPROP_XSIZE,w*cols+15);
   ObjectSetInteger(0,"PANEL_BG_SUB",OBJPROP_YSIZE,rows*20+40);
   ObjectSetInteger(0,"PANEL_BG_SUB",OBJPROP_BGCOLOR,C'30,30,30');
   
   ObjectCreate(0,"PANEL_TITLE_SUB",OBJ_LABEL,0,0,0);
   ObjectSetString(0,"PANEL_TITLE_SUB",OBJPROP_TEXT,"2. SUB-TYPE YA "+MainMaterials[mainIndex]);
   ObjectSetInteger(0,"PANEL_TITLE_SUB",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"PANEL_TITLE_SUB",OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,"PANEL_TITLE_SUB",OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,"PANEL_TITLE_SUB",OBJPROP_COLOR,clrGold);
   
   for(int i=0; i<ArraySize(subArray); i++){
      int col = i % cols;
      int row = i / cols;
      string name = "BTN_SUB_"+subArray[i];
      ObjectCreate(0,name,OBJ_BUTTON,0,0,0);
      ObjectSetInteger(0,name,OBJPROP_CORNER,CORNER_LEFT_UPPER);
      ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x+col*(w+2));
      ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y+25+row*20);
      ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
      ObjectSetInteger(0,name,OBJPROP_YSIZE,h);
      ObjectSetString(0,name,OBJPROP_TEXT,subArray[i]);
      ObjectSetInteger(0,name,OBJPROP_BGCOLOR,clrDimGray);
      ObjectSetInteger(0,name,OBJPROP_COLOR,clrWhite);
      ObjectSetInteger(0,name,OBJPROP_FONTSIZE,7);
   }
}

void CreateQtyPanel(){
   int x=480,y=20,w=150,h=20;
   
   ObjectCreate(0,"PANEL_BG_QTY",OBJ_RECTANGLE_LABEL,0,0,0);
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_XDISTANCE,x-5);
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_YDISTANCE,y-5);
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_XSIZE,w+10);
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_YSIZE,200);
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_BGCOLOR,C'40,40,40');
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_HIDDEN,true);
   
   ObjectCreate(0,"PANEL_TITLE_QTY",OBJ_LABEL,0,0,0);
   ObjectSetString(0,"PANEL_TITLE_QTY",OBJPROP_TEXT,"3. QUANTITY - MAX 999M");
   ObjectSetInteger(0,"PANEL_TITLE_QTY",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"PANEL_TITLE_QTY",OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,"PANEL_TITLE_QTY",OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,"PANEL_TITLE_QTY",OBJPROP_COLOR,clrCyan);
   ObjectSetInteger(0,"PANEL_TITLE_QTY",OBJPROP_HIDDEN,true);
   
   ObjectCreate(0,"EDIT_QTY",OBJ_EDIT,0,0,0);
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_YDISTANCE,y+25);
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_XSIZE,w);
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_YSIZE,h+5);
   ObjectSetString(0,"EDIT_QTY",OBJPROP_TEXT,IntegerToString(DefaultQty));
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_ALIGN,ALIGN_CENTER);
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_HIDDEN,true);
   
   string btns[] = {"BTN_QTY_ADD","+1","BTN_QTY_SUB","-1","BTN_QTY_X10","+10","BTN_QTY_X100","+100","BTN_QTY_X1000","+1000","BTN_QTY_SAVE","SAVE"};
   for(int i=0; i<ArraySize(btns); i+=2){
      ObjectCreate(0,btns[i],OBJ_BUTTON,0,0,0);
      ObjectSetInteger(0,btns[i],OBJPROP_CORNER,CORNER_LEFT_UPPER);
      ObjectSetInteger(0,btns[i],OBJPROP_XDISTANCE,x+(i/2%2)*75);
      ObjectSetInteger(0,btns[i],OBJPROP_YDISTANCE,y+55+(i/4)*25);
      ObjectSetInteger(0,btns[i],OBJPROP_XSIZE,70);
      ObjectSetInteger(0,btns[i],OBJPROP_YSIZE,h);
      ObjectSetString(0,btns[i],OBJPROP_TEXT,btns[i+1]);
      ObjectSetInteger(0,btns[i],OBJPROP_HIDDEN,true);
   }
}

void CreateExcelButton(){
   ObjectCreate(0,"BTN_EXPORT",OBJ_BUTTON,0,0,0);
   ObjectSetInteger(0,"BTN_EXPORT",OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,"BTN_EXPORT",OBJPROP_XDISTANCE,480);
   ObjectSetInteger(0,"BTN_EXPORT",OBJPROP_YDISTANCE,250);
   ObjectSetInteger(0,"BTN_EXPORT",OBJPROP_XSIZE,150);
   ObjectSetInteger(0,"BTN_EXPORT",OBJPROP_YSIZE,25);
   ObjectSetString(0,"BTN_EXPORT",OBJPROP_TEXT,"📊 EXPORT TO EXCEL");
   ObjectSetInteger(0,"BTN_EXPORT",OBJPROP_BGCOLOR,clrGreen);
   ObjectSetInteger(0,"BTN_EXPORT",OBJPROP_COLOR,clrWhite);
}

//+------------------------------------------------------------------+
void GetSubTypes(int idx, string &arr[]){
   ArrayResize(arr,0);
   if(idx==0) ArrayCopy(arr,SubTypes_CEMENT);
   if(idx==1) ArrayCopy(arr,SubTypes_SAND);
   if(idx==2) ArrayCopy(arr,SubTypes_GRAVEL);
   if(idx==3) ArrayCopy(arr,SubTypes_STEEL_BAR);
   if(idx==4) ArrayCopy(arr,SubTypes_BRICKS);
   if(idx==5) ArrayCopy(arr,SubTypes_TIMBER);
   if(idx==6) ArrayCopy(arr,SubTypes_IRON_SHEET);
   if(idx==7) ArrayCopy(arr,SubTypes_PAINT);
   if(idx==8) ArrayCopy(arr,SubTypes_TILES);
   if(idx==9) ArrayCopy(arr,SubTypes_NAILS);
   if(idx==10) ArrayCopy(arr,SubTypes_CONCRETE);
   if(idx==11) ArrayCopy(arr,SubTypes_GLASS);
   if(idx==12) ArrayCopy(arr,SubTypes_PVC_PIPES);
   if(idx==13) ArrayCopy(arr,SubTypes_WIRES);
   if(idx==14) ArrayCopy(arr,SubTypes_BLOCKS);
   if(idx==15) ArrayCopy(arr,SubTypes_WATERPROOF);
   if(idx==16) ArrayCopy(arr,SubTypes_CEILING);
   if(idx==17) ArrayCopy(arr,SubTypes_DOORS);
   if(idx==18) ArrayCopy(arr,SubTypes_WINDOWS);
   if(idx==19) ArrayCopy(arr,SubTypes_AGGREGATE);
}

void HighlightMainButton(int index){
   for(int i=0; i<ArraySize(MainMaterials); i++){
      string name = "BTN_MAIN_"+MainMaterials[i];
      ObjectSetInteger(0,name,OBJPROP_BGCOLOR, i==index? clrDodgerBlue : clrDarkGray);
   }
}

void HighlightSubButton(string btnName){
   string subArray[]; GetSubTypes(SelectedMainIndex, subArray);
   for(int i=0; i<ArraySize(subArray); i++){
      string name = "BTN_SUB_"+subArray[i];
      ObjectSetInteger(0,name,OBJPROP_BGCOLOR, name==btnName? clrLime : clrDimGray);
   }
}

void ChangeQty(int delta){
   SelectedQty += delta;
   if(SelectedQty<0) SelectedQty=0;
   if(SelectedQty>MaxQuantity) SelectedQty=MaxQuantity;
   UpdateQtyDisplay();
}

void UpdateQtyDisplay(){ ObjectSetString(0,"EDIT_QTY",OBJPROP_TEXT,IntegerToString(SelectedQty)); }
void DeleteSubPanel(){ ObjectsDeleteAll(0,"PANEL_BG_SUB"); ObjectsDeleteAll(0,"PANEL_TITLE_SUB"); ObjectsDeleteAll(0,"BTN_SUB_"); }
void ShowQtyPanel(){
   ObjectSetInteger(0,"PANEL_BG_QTY",OBJPROP_HIDDEN,false);
   ObjectSetInteger(0,"PANEL_TITLE_QTY",OBJPROP_HIDDEN,false);
   ObjectSetInteger(0,"EDIT_QTY",OBJPROP_HIDDEN,false);
   string btns[] = {"BTN_QTY_ADD","BTN_QTY_SUB","BTN_QTY_X10","BTN_QTY_X100","BTN_QTY_X1000","BTN_QTY_SAVE"};
   for(int i=0; i<ArraySize(btns); i++) ObjectSetInteger(0,btns[i],OBJPROP_HIDDEN,false);
   SelectedQty = DefaultQty;
   UpdateQtyDisplay();
}

void UpdateInfoPanel(){
   if(SelectedMain!="" && SelectedSub!=""){
      Comment("SELECTED: ",SelectedMain," -> ",SelectedSub," | QTY: ",IntegerToString(SelectedQty)," | Exports: ",ExportCount);
   }
}

double GetDrawingScaleMM(){
   int bars = WindowBarsPerChart();
   double high = High[iHighest(NULL,0,MODE_HIGH,bars,0)];
   double low = Low[iLowest(NULL,0,MODE_LOW,bars,0)];
   return (high - low) / Point;
}

void SaveCurrentSelection(){
   GlobalVariableSet("BES_Main",SelectedMainIndex);
   GlobalVariableSet("BES_Sub",SelectedSub);
   GlobalVariableSet("BES_Qty",SelectedQty);
   Alert("SAVED: "+SelectedMain+"->"+SelectedSub+" Qty:"+IntegerToString(SelectedQty));
}

void LoadSavedSelection(){
   if(GlobalVariableCheck("BES_Main")){
      SelectedMainIndex = (int)GlobalVariableGet("BES_Main");
      SelectedMain = MainMaterials[SelectedMainIndex];
      SelectedSub = GlobalVariableGet("BES_Sub");
      SelectedQty = (long)GlobalVariableGet("BES_Qty");
      HighlightMainButton(SelectedMainIndex);
      CreateSubPanel(SelectedMainIndex);
      ShowQtyPanel();
   }
}

void SaveSelection(){ if(SelectedMain!="") SaveCurrentSelection(); }
bool IsNewCandle(){ static datetime lastBar=0; if(Time[0]!=lastBar){lastBar=Time[0]; return true;} return false; }
//+------------------------------------------------------------------+
