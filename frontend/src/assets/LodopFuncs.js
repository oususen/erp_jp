var CreatedOKLodop7766=null;

//====CLodopクラウド印刷サーバーのインストール必要性確認:====
export function needCLodop(){
  try{
    var ua=navigator.userAgent;
    if (ua.match(/Windows\sPhone/i) !=null) return true;
    if (ua.match(/iPhone|iPod/i) != null) return true;
    if (ua.match(/Android/i) != null) return true;
    if (ua.match(/Edge\D?\d+/i) != null) return true;

    var verTrident=ua.match(/Trident\D?\d+/i);
    var verIE=ua.match(/MSIE\D?\d+/i);
    var verOPR=ua.match(/OPR\D?\d+/i);
    var verFF=ua.match(/Firefox\D?\d+/i);
    var x64=ua.match(/x64/i);
    if ((verTrident==null)&&(verIE==null)&&(x64!==null))
      return true; else
    if ( verFF !== null) {
      verFF = verFF[0].match(/\d+/);
      if ((verFF[0]>= 42)||(x64!==null)) return true;
    } else
    if ( verOPR !== null) {
      verOPR = verOPR[0].match(/\d+/);
      if ( verOPR[0] >= 32 ) return true;
    } else
    if ((verTrident==null)&&(verIE==null)) {
      var verChrome=ua.match(/Chrome\D?\d+/i);
      if ( verChrome !== null ) {
        verChrome = verChrome[0].match(/\d+/);
        if (verChrome[0]>=42) return true;
      };
    };
    return false;
  } catch(err) {return true;};
};

//====ページでCLodopクラウド印刷に必要なJSファイルを参照：====
if (needCLodop()) {
  var head = document.head || document.getElementsByTagName("head")[0] || document.documentElement;
  var oscript = document.createElement("script");
  oscript.src ="http://localhost:8000/CLodopfuncs.js?priority=1";
  head.insertBefore( oscript,head.firstChild );

  //二重ポート(8000と18000)を参照し、いずれかが占有されるのを防ぎます
  oscript = document.createElement("script");
  oscript.src ="http://localhost:18000/CLodopfuncs.js?priority=0";
  head.insertBefore( oscript,head.firstChild );
};

//====LODOPオブジェクト取得の主な手順：====
export function getLodop(oOBJECT,oEMBED){
  var strHtmInstall="<br><font color='#FF00FF'>印刷コントロール未インストール!ここをクリック<a href='install_lodop32.exe' target='_self'>インストール実行</a>,インストール後はページを更新または再アクセスしてください</font>";
  var strHtmUpdate="<br><font color='#FF00FF'>印刷コントロールのアップグレード必要!ここをクリック<a href='install_lodop32.exe' target='_self'>アップグレード実行</a>,アップグレード後は再アクセスしてください</font>";
  var strHtm64_Install="<br><font color='#FF00FF'>印刷コントロール未インストール!ここをクリック<a href='install_lodop64.exe' target='_self'>インストール実行</a>,インストール後はページを更新または再アクセスしてください</font>";
  var strHtm64_Update="<br><font color='#FF00FF'>印刷コントロールのアップグレード必要!ここをクリック<a href='install_lodop64.exe' target='_self'>アップグレード実行</a>,アップグレード後は再アクセスしてください</font>";
  var strHtmFireFox="<br><br><font color='#FF00FF'>（注意：以前にLodop旧版アドオンnpActiveXPLuginをインストールした場合,【ツール】で->【アドオン】->【拡張機能】先にアンインストールしてください</font>";
  var strHtmChrome="<br><br><font color='#FF00FF'>(以前正常でブラウザのアップグレードまたは再インストールのみが原因の場合、上記のインストールを再実行する必要があります</font>";
  var strCLodopInstall="<br><font color='#FF00FF'>CLodopクラウド印刷サービス（localhostローカル）がインストールされていません!ここをクリック<a href='http://www.c-lodop.com/download/CLodop_Setup_for_Win32NT_https_3.008Extend.zip' target='_self'>インストール実行</a>,インストール後はページを更新してください</font>";
  var strCLodopUpdate="<br><font color='#FF00FF'>CLodopクラウド印刷サービスのアップグレードが必要!ここをクリック<a href='CLodop_Setup_for_Win32NT.exe' target='_self'>アップグレード実行</a>,アップグレード後はページを更新してください</font>";
  var LODOP;
  try{
    var isIE = (navigator.userAgent.indexOf('MSIE')>=0) || (navigator.userAgent.indexOf('Trident')>=0);
    if (needCLodop()) {
      try{ LODOP=getCLodop();} catch(err) {};
      if (!LODOP && document.readyState!=="complete") {alert("C-Lodop準備ができていません。後でもう一度お試しください"); return;};
      if (!LODOP) {
        // if (isIE) document.write(strCLodopInstall); else
          // document.documentElement.innerHTML=strCLodopInstall+document.documentElement.innerHTML;
        // return;
      } else {

        if (CLODOP.CVERSION<"3.0.0.2") {
          if (isIE) document.write(strCLodopUpdate); else
            document.documentElement.innerHTML=strCLodopUpdate+document.documentElement.innerHTML;
        };
        if (oEMBED && oEMBED.parentNode) oEMBED.parentNode.removeChild(oEMBED);
        if (oOBJECT && oOBJECT.parentNode) oOBJECT.parentNode.removeChild(oOBJECT);
      };
    } else {
      var is64IE  = isIE && (navigator.userAgent.indexOf('x64')>=0);
      //=====ページにLodopがある場合は直接使用し、ない場合は新規作成します:==========
      if (oOBJECT!=undefined || oEMBED!=undefined) {
        if (isIE) LODOP=oOBJECT; else  LODOP=oEMBED;
      } else if (CreatedOKLodop7766==null){
        LODOP=document.createElement("object");
        LODOP.setAttribute("width",0);
        LODOP.setAttribute("height",0);
        LODOP.setAttribute("style","position:absolute;left:0px;top:-100px;width:0px;height:0px;");
        if (isIE) LODOP.setAttribute("classid","clsid:2105C259-1E0C-4534-8141-A753534CB4CA");
        else LODOP.setAttribute("type","application/x-print-lodop");
        document.documentElement.appendChild(LODOP);
        CreatedOKLodop7766=LODOP;
      } else LODOP=CreatedOKLodop7766;
      //=====Lodopプラグイン未インストール時のダウンロードURL表示:==========
      if ((LODOP==null)||(typeof(LODOP.VERSION)=="undefined")) {
        if (navigator.userAgent.indexOf('Chrome')>=0)
          document.documentElement.innerHTML=strHtmChrome+document.documentElement.innerHTML;
        if (navigator.userAgent.indexOf('Firefox')>=0)
          document.documentElement.innerHTML=strHtmFireFox+document.documentElement.innerHTML;
        if (is64IE) document.write(strHtm64_Install); else
        if (isIE)   document.write(strHtmInstall);    else
          document.documentElement.innerHTML=strHtmInstall+document.documentElement.innerHTML;
        return LODOP;
      };
    };
    if (LODOP.VERSION<"6.0") {
      if (!needCLodop()){
        if (is64IE) document.write(strHtm64_Update); else
        if (isIE) document.write(strHtmUpdate); else
          document.documentElement.innerHTML=strHtmUpdate+document.documentElement.innerHTML;
      };
      return LODOP;
    };
    //===次の日白の位置は、統合機能 (登録ステートメント、言語選択など) を呼び出すのに適しています。:===
    //LODOP.SET_LICENSES("北京XXXXX会社","8xxxxxxxxxxxxx5","","");

    //===========================================================
    return LODOP;
  } catch(err) {alert("getLodopエラー発生発生:まずLodopをインストールしてください,ダウンロードURL："+'http://www.lodop.net/download/CLodop_Setup_for_Win64NT_4.142EN.zip');};
};
