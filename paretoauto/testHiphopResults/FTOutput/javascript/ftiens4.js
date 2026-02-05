//**************************************************************** 
// You must keep this copyright notice:
//
// This script is Copyright (c) 2006 by Conor O'Mahony.
// For inquiries, please email GubuSoft@GubuSoft.com.
// GubuSoft is owned and operated by Conor O'Mahony.
//
// Do not download the script's files from here.  For a free 
// download and full instructions go to the following site: 
// http://www.TreeView.net
//**************************************************************** 

// Log of changes: 
//      29 Apr 25 - Fixed bug where in Chromium based browsers returning to the fault tree view 
//                  resulted in strange behaviour where you couldn't expand the tree using the +/-
//                  buttons. The fix was resetting of the global variables that are otherwise only 
//                  visited once when the page loads.
//                  Additionally, code has been revised and refactored to remove legacy unused blocks.
//      26 Sep 06 - Updated preLoadIcons function;
//                  Fix small bugs or typos (in the Folder, InitializeFolder,
//                  and blockStartHTML functions)
//      14 Feb 06 - Rebrand as GubuSoft
//      08 Jun 04 - Very small change to one error message
//      21 Mar 04 - Support for folder.addChildren allows for much bigger trees
//      12 May 03 - Support for Safari Beta 3
//      01 Mar 03 - VERSION 4.3 - Support for checkboxes
//      21 Feb 03 - Added support for Opera 7
//      22 Sep 02 - Added maySelect member for node-by-node control
//                  of selection and highlight
//      21 Sep 02 - Cookie values are now separated by cookieCutter
//      12 Sep 02 - VERSION 4.2 - Can highlight Selected Nodes and 
//                  can preserve state through external (DB) IDs
//      29 Aug 02 - Fine tune 'supportDeferral' for IE4 and IE Mac
//      25 Aug 02 - Fixes: STARTALLOPEN, and multi-page frameless
//      09 Aug 02 - Fix repeated folder on Mozilla 1.x
//      31 Jul 02 - VERSION 4.1 - Dramatic speed increase for trees 
//      with hundreds or thousands of nodes; changes to the control
//      flags of the gLnk function
//      18 Jul 02 - Changes in pre-load images function
//      13 Jun 02 - Add ICONPATH var to allow for gif subdir
//      20 Apr 02 - Improve support for frame-less layout
//      07 Apr 02 - Minor changes to support server-side dynamic feeding
//                  (example: FavoritesManagerASP)

 
// Definition of class Folder 
// ***************************************************************** 
function Folder(folderDescription, hreference) //constructor 
{ 
  //constant data 
  this.desc = folderDescription; 
  this.hreference = hreference;
  this.id = -1;
  this.navObj = 0;
  this.iconImg = 0; 
  this.nodeImg = 0;
  this.iconSrc = ICONPATH + "ftv2folderopen.gif";
  this.iconSrcClosed = ICONPATH + "ftv2folderclosed.gif";
  this.children = new Array;
  this.nChildren = 0;
  this.level = 0;
  this.leftSideCoded = "";
  this.isLastNode=false;
  this.parentObj = null;
  this.maySelect=true;
  this.prependHTML = "";
 
  //dynamic data 
  this.isOpen = false;
  this.isLastOpenedFolder = false;
  this.isRendered = 0;
 
  //methods 
  this.initialize = initializeFolder;
  this.setState = setStateFolder;
  this.addChild = addChild;
  this.addChildren = addChildren;
  this.createIndex = createEntryIndex;
  this.hideBlock = hideBlock;
  this.hide = hideFolder;
  this.folderMstr = folderMstr;
  this.renderOb = drawFolder;
  this.totalHeight = totalHeight;
  this.subEntries = countFolderSubEntries ;
  this.linkHTML = linkFolderHTML;
  this.blockStartHTML = blockStartHTML;
  this.blockEndHTML = blockEndHTML;
  this.nodeImageSrc = nodeImageSrc;
  this.iconImageSrc = iconImageSrc;
  this.getID = getID;
  this.forceOpeningOfAncestorFolders = forceOpeningOfAncestorFolders;
} 
 
function initializeFolder(level, lastNode, leftSide) 
{ 
  nc = this.nChildren; 
   
  this.createIndex();
  this.level = level;
  this.leftSideCoded = leftSide;
  
  if (level>0) {
    if (lastNode) {//the last child in the children array 
		  leftSide = leftSide + "0";
    }  
    else {
      leftSide = leftSide + "1";
    }
  }
  this.isLastNode = lastNode;
 
  if (nc > 0) 
  { 
    level = level + 1;
    for (let i=0 ; i < this.nChildren; i++)  
    {
      if (typeof this.children[i].initialize == 'undefined') //document node was specified using the addChildren function
      {
        if (typeof this.children[i][0] == 'undefined' || typeof this.children[i] == 'string')
        {
          this.children[i] = ["item incorrectly defined", ""];
        }

        //Basic initialization of the Item object
        //These members or methods are needed even before the Item is rendered
        this.children[i].initialize=initializeItem;
        this.children[i].createIndex=createEntryIndex;
        if (typeof this.children[i].maySelect == 'undefined') {
          this.children[i].maySelect=true;
        }
        this.children[i].forceOpeningOfAncestorFolders = forceOpeningOfAncestorFolders;
      }
      if (i == this.nChildren-1) {
        this.children[i].initialize(level, 1, leftSide);
      }
      else { 
        this.children[i].initialize(level, 0, leftSide);
      }
    } 
  } 
} 
 
function drawFolder(insertAtObj) 
{ 
  let nodeName = "";
  let auxEv = "";
  let docW = "";

  finalizeCreationOfChildDocs(this);

  let leftSide = leftSideHTML(this.leftSideCoded);

  auxEv = "<a href='javascript:clickOnNode(\""+this.getID()+"\")'>";
  
  nodeName = this.nodeImageSrc();
 
  if (this.level>0) {
    if (this.isLastNode) { //the last child in the children array 
	    leftSide = leftSide + "<td valign=top>" + auxEv + "<img name='nodeIcon" + this.id + "' id='nodeIcon" + this.id + "' src='" + nodeName + "' width=16 height=22 border=0></a></td>";
    }
    else { 
      leftSide = leftSide + "<td valign=top background=" + ICONPATH + "ftv2vertline.gif>" + auxEv + "<img name='nodeIcon" + this.id + "' id='nodeIcon" + this.id + "' src='" + nodeName + "' width=16 height=22 border=0></a></td>";
    }
  }
  this.isRendered = 1;

  docW = this.blockStartHTML("folder");

  docW = docW + "<tr>" + leftSide + "<td valign=top>";
  if (USEICONS)
  {
    docW = docW + this.linkHTML(false);
    docW = docW + "<img id='folderIcon" + this.id + "' name='folderIcon" + this.id + "' src='" + this.iconImageSrc() + "' border=0></a>";
  }
  else
  {
	  if (this.prependHTML == "") {
        docW = docW + "<img src=" + ICONPATH + "ftv2blank.gif height=2 width=2>";
    }
  }
  if (WRAPTEXT) {
	  docW = docW + "</td>"+this.prependHTML+"<td valign=middle width=100%>";
  }
  else {
	  docW = docW + "</td>"+this.prependHTML+"<td valign=middle nowrap width=100%>";
  }
  if (USETEXTLINKS) 
  { 
    docW = docW + this.linkHTML(true);
    docW = docW + this.desc + "</a>";
  } 
  else {
    docW = docW + this.desc;
  }
  docW = docW + "</td>";

  docW = docW + this.blockEndHTML();

  if (insertAtObj == null)
  {
	  //doc.write("<div id=domRoot></div>") //transition between regular flow HTML, and node-insert DOM DHTML
    // as we are dynamically loading the tree view with the page already loaded doc.write overwrites the whole page
      // not what we want. 
    let monkey = doc.getElementById('TreeviewSpanZone');
    let ss = document.createElement('div');
    ss.id = "domRoot";
    monkey.appendChild(ss);
          // end of David's patch
    insertAtObj = doc.getElementById("domRoot");
    insertAtObj.insertAdjacentHTML("beforeEnd", docW);	  
  }
  else
  {
      insertAtObj.insertAdjacentHTML("afterEnd", docW);
  }
 
  this.navObj = doc.getElementById("folder"+this.id);
  if (USEICONS) {
    this.iconImg = doc.getElementById("folderIcon"+this.id);
  }
  this.nodeImg = doc.getElementById("nodeIcon"+this.id);
  
} 
 
function setStateFolder(isOpen) 
{ 
  if (isOpen == this.isOpen) {
    return;
  }    
  this.isOpen = isOpen;

  if (!this.isOpen && this.isLastOpenedfolder)
  {
		lastOpenedFolder = null;
		this.isLastOpenedfolder = false;
  }
  propagateChangesInState(this);
} 
 
function propagateChangesInState(folder) 
{   
  //Change icon
  if (folder.nChildren > 0 && folder.level > 0) {  //otherwise the one given at render stays
    folder.nodeImg.src = folder.nodeImageSrc();
  }

  //Change node
  if (USEICONS) {
    folder.iconImg.src = folder.iconImageSrc();
  }

  //Propagate changes
  for (let i = folder.nChildren-1; i>=0; i--) {
    if (folder.isOpen) {
      folder.children[i].folderMstr(folder.navObj);
    }
    else { 
  	  folder.children[i].hide();
    }
  }
} 
 
function hideFolder() 
{ 
  this.hideBlock();   
  this.setState(0);
} 
 
function linkFolderHTML(isTextLink) 
{ 
  let docW = "";

  if (this.hreference) 
  { 
    if (USEFRAMES){
      docW = docW + "<a href='" + this.hreference + "' ";
    }
    else {
      docW = docW + "<a href='" + this.hreference + "' ";
    }
          
    if (isTextLink) {
        docW += "id=\"itemTextLink"+this.id+"\" ";
    }

    docW = docW + "onClick='javascript:clickOnFolder(\""+this.getID()+"\")'>";
  } 
  else { 
    docW = docW + "<a>";
  }

  return docW;
} 
 
function addChild(childNode) 
{ 
  this.children[this.nChildren] = childNode; 
  childNode.parentObj = this;
  this.nChildren++; 
  return childNode; 
} 

//The list can contain either a Folder object or a sub list with the arguments for Item 
function addChildren(listOfChildren) 
{ 
  this.children = listOfChildren;
  this.nChildren = listOfChildren.length;
  for (let i = 0; i<this.nChildren; i++) {
    this.children[i].parentObj = this;
  }
} 

function countFolderSubEntries() 
{ 
  let count = this.nChildren;
 
  for (let i = 0; i < this.nChildren; i++) { 
    if (this.children[i].children) { //is a folder 
      count = count + this.children[i].subEntries();
    }
  } 
 
  return count; 
} 

function nodeImageSrc() {
  let srcStr = "";

  if (this.isLastNode) //the last child in the children array 
  { 
    if (this.nChildren == 0) {
      srcStr = ICONPATH + "ftv2lastnode.gif";
    }
    else {
      if (this.isOpen) {
        srcStr = ICONPATH + "ftv2mlastnode.gif"; 
      }
      else {
        srcStr = ICONPATH + "ftv2plastnode.gif";  
      }
    } 
  } 
  else 
  { 
    if (this.nChildren == 0) {
      srcStr = ICONPATH + "ftv2node.gif";
    }
    else {
      if (this.isOpen) {
        srcStr = ICONPATH + "ftv2mnode.gif";
      }
      else {
        srcStr = ICONPATH + "ftv2pnode.gif";
      }
    }
  }   
  return srcStr;
}

function iconImageSrc() {
  if (this.isOpen) {
    return(this.iconSrc);
  }
  else {
    return(this.iconSrcClosed);
  }
} 
 
// Methods common to both objects (pseudo-inheritance) 
// ******************************************************** 
 
function forceOpeningOfAncestorFolders() {
  if (this.parentObj == null || this.parentObj.isOpen) {
    return;
  }
  else {
    this.parentObj.forceOpeningOfAncestorFolders();
    clickOnNodeObj(this.parentObj);
  }
}

function hideBlock() 
{ 
  if (this.navObj.style.display == "none") {
      return;
  }
  else { 
    this.navObj.style.display = "none";
  } 
   
} 
 
function folderMstr(domObj) 
{ 
  if (!this.isRendered) {
     this.renderOb(domObj);
  }
  else {
    this.navObj.style.display = "block";
  }
} 

function blockStartHTML(idprefix) {
  let idParam = "id='" + idprefix + this.id + "'";
  let docW = "";

  docW = "<div " + idParam + " style='display:block;'>";     
  docW = docW + "<table border=0 cellspacing=0 cellpadding=0 width=100% >";

  return docW;
}

function blockEndHTML() {
  return "</table></div>";
}
 
function createEntryIndex() 
{ 
  this.id = nEntries;
  indexOfEntries[nEntries] = this;
  nEntries++;
} 
 
// total height of subEntries open 
function totalHeight() 
{ 
  let height = this.navObj.clip.height;   
  if (this.isOpen) { //is a folder and _is_ open 
    for (let i=0 ; i < this.nChildren; i++) {
      height = height + this.children[i].totalHeight();
    } 
  } 
  return height; 
} 


function leftSideHTML(leftSideCoded) {
	let retStr = "";

	for (let i=0; i<leftSideCoded.length; i++)
	{
		if (leftSideCoded.charAt(i) == "1")
		{
			retStr = retStr + "<td valign=top background=" + ICONPATH + "ftv2vertline.gif><img src='" + ICONPATH + "ftv2vertline.gif' width=16 height=22></td>";
		}
		if (leftSideCoded.charAt(i) == "0")
		{
			retStr = retStr + "<td valign=top><img src='" + ICONPATH + "ftv2blank.gif' width=16 height=22></td>";
		}
	}
	return retStr;
}

function getID()
{
  //define a .xID in all nodes (folders and items) if you want to PERVESTATE that
  //work when the tree changes. The value eXternal value must be unique for each
  //node and must node change when other nodes are added or removed
  //The value may be numeric or string, but cannot have the same char used in cookieCutter
  if (typeof this.xID != "undefined") {
    return this.xID;
  }
  else {
    return this.id;
  }
}

 
// Events 
// ********************************************************* 
 
function clickOnFolder(folderId) 
{ 
  let clicked = findObj(folderId);

  if (typeof clicked=='undefined' || clicked==null)
  {
    alert("Treeview was not able to find the node object corresponding to ID=" + folderId + ". If the configuration file sets a.xID values, it must set them for ALL nodes, including the foldersTree root.")
    return;
  }

  if (!clicked.isOpen) {
    clickOnNodeObj(clicked);
  }

  if (lastOpenedFolder != null && lastOpenedFolder != folderId)
    clickOnNode(lastOpenedFolder); //sets lastOpenedFolder to null

  if (clicked.nChildren==0) {
    lastOpenedFolder = folderId;
    clicked.isLastOpenedfolder = true;
  }

  if (isLinked(clicked.hreference)) {
      highlightObjLink(clicked);
  }
} 
 
function clickOnNode(folderId) 
{ 
  let fOb = findObj(folderId);
  if (typeof fOb=='undefined' || fOb==null)
  {
    alert("Treeview was not able to find the node object corresponding to ID=" + folderId + ". If the configuration file sets a.xID, it must set foldersTree.xID as well.")
    return;
  }
  clickOnNodeObj(fOb);
}

function clickOnNodeObj(folderObj) 
{ 
  let state = folderObj.isOpen;
  folderObj.setState(!state); //open<->close  
}

function clickOnLink(clickedId, target, windowName) {
    highlightObjLink(findObj(clickedId));
    if (isLinked(target)) {
        window.open(target,windowName);
    }
}

function ld  ()
{
	return document.links.length-1;
}
 

// Auxiliary Functions 
// *******************

function finalizeCreationOfChildDocs(folderObj) {
  for(let i = 0; i < folderObj.nChildren; i++)  {
    child = folderObj.children[i];
    if (typeof child[0] != 'undefined')
    {
      // Amazingly, arrays can have members, so   a = ["a", "b"]; a.desc="asdas"   works
      // If a doc was inserted as an array, we can transform it into an itemObj by adding 
      // the missing members and functions
      child.desc = child[0];
      setItemLink(child, GLOBALTARGET, child[1]);  
      finalizeCreationOfItem(child);
    }
  }
}

function findObj(id)
{
 if (typeof foldersTree.xID != "undefined") {
    for(let i = 0;i<nEntries;i++) { //may need optimization
      if(indexOfEntries[i].xID==id) {
        return indexOfEntries[i];
      }
    }
  }
  // not found
  return null;   
}

function isLinked(hrefText) {
    let result = true;
    result = (result && hrefText !=null);
    result = (result && hrefText != '');
    result = (result && hrefText.indexOf('undefined') < 0);
    result = (result && hrefText.indexOf('parent.op') < 0);
    return result;
}

// Do highlighting by changing background and foreg. colors of folder or doc text
function highlightObjLink(nodeObj) {
  if (!HIGHLIGHT || nodeObj==null || nodeObj.maySelect==false) {//node deleted in DB 
    return;
  }

  
  let clickedDOMObj = doc.getElementById('itemTextLink'+nodeObj.id);
  if (clickedDOMObj != null) {
      if (lastClicked != null) {
          let prevClickedDOMObj = doc.getElementById('itemTextLink'+lastClicked.id);
          prevClickedDOMObj.style.color=lastClickedColor;
          prevClickedDOMObj.style.backgroundColor=lastClickedBgColor;
      }
      
      lastClickedColor    = clickedDOMObj.style.color;
      lastClickedBgColor  = clickedDOMObj.style.backgroundColor;
      clickedDOMObj.style.color=HIGHLIGHT_COLOR;
      clickedDOMObj.style.backgroundColor=HIGHLIGHT_BG;
  }
  
  lastClicked = nodeObj;
  
}

function insFld(parentFolder, childFolder) 
{ 
  return parentFolder.addChild(childFolder) 
} 
 
function insDoc(parentFolder, document) 
{ 
  return parentFolder.addChild(document) 
} 

function gFld(description, hreference) 
{ 
  let folder = new Folder(description, hreference);
  return folder;
} 


 
function preLoadIcons() {
       arImageSrc = new Array (
           "ftv2vertline.gif",
           "ftv2mlastnode.gif",
           "ftv2mnode.gif",
           "ftv2plastnode.gif",
           "ftv2pnode.gif",
           "ftv2blank.gif",
           "ftv2lastnode.gif",
           "ftv2node.gif"
           )
       arImageList = new Array ();
       for (counter in arImageSrc) {
           arImageList[counter] = new Image();
           arImageList[counter].src = ICONPATH + arImageSrc[counter];
       }
   }

//Open some folders for initial layout, if necessary
function setInitialLayout() {
  if (!STARTALLOPEN)
    clickOnNodeObj(foldersTree);
}

//To customize the tree, overwrite these variables in the configuration file (demoFramesetNode.js, etc.)
var USETEXTLINKS = 0;
var STARTALLOPEN = 0;
var USEFRAMES = 1;
var USEICONS = 1;
var WRAPTEXT = 0;
var ICONPATH = '';
var HIGHLIGHT = 0;
var HIGHLIGHT_COLOR = 'white';
var HIGHLIGHT_BG    = 'blue';
var BUILDALL = 0;
var GLOBALTARGET = "R"; // variable only applicable for addChildren uses


//Other variables
var lastClicked = null;
var lastClickedColor;
var lastClickedBgColor;
var indexOfEntries = new Array 
var nEntries = 0; 
var selectedFolder = 0;
var lastOpenedFolder = null;
var t=5;
var doc = document;
doc.yPos = 0;

function resetGlobalVariables()
{
  lastClicked = null;
  lastClickedColor;
  lastClickedBgColor;
  indexOfEntries = new Array 
  nEntries = 0; 
  selectedFolder = 0;
  lastOpenedFolder = null;
  t=5;
  doc = document;
  doc.yPos = 0;
}
// Main function
// ************* 

// This function uses an object (navigator) defined in
// ua.js, imported in the main html page (left frame).
function initializeDocument() 
{ 
  resetGlobalVariables();
  preLoadIcons();
   
  //foldersTree (with the site's data) is created in an external .js (demoFramesetNode.js, for example)
  foldersTree.initialize(0, true, ""); 
  foldersTree.renderOb(null); //delay construction of nodes
  
  setInitialLayout(); 
}

function toggleAllFolders(folder) {
    //  folder.setState(false);
    for (let i = folder.nChildren - 1; i >= 0; i--) {
        toggleAllSubFolders(folder.children[i]);
    }
}
function toggleAllSubFolders(folder) {
    if (!folder.isOpen) {
        folder.setState(true);
        for (let i = folder.nChildren - 1; i >= 0; i--) {
          toggleAllSubFolders(folder.children[i]);
        }
    }
    else {
        folder.setState(false);
    }
}

function openAllFolders(folder) {
    //  folder.setState(true);
    for (let i = folder.nChildren - 1; i >= 0; i--) {
        openAllSubFolders(folder.children[i]);
    }
}
function openAllSubFolders(folder) {
    folder.setState(true);
    for (let i = folder.nChildren - 1; i >= 0; i--) {
        openAllSubFolders(folder.children[i]);
    }
}