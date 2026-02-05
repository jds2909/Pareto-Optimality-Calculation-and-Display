function changeTitle(newTitle) {
    document.title = newTitle;
}

function runTransform(xmlString, xslString, nodeToTransformId, parameters) {
    try {
       if (window.DOMParser || "DOMParser" in window) {
                          const xslParser = new DOMParser();
            const xslProc = new XSLTProcessor();
            const xslDoc = xslParser.parseFromString(xslString, "text/xml");
           xslProc.importStylesheet(xslDoc);
           const xmlParser = new DOMParser();
           const xmlDoc = xmlParser.parseFromString(xmlString, "text/xml");
           
            if (parameters != "") { //Loop through the parameters and apply each to the XSLT Processor
                for (Index in parameters) {
                    xslProc.setParameter(null, parameters[Index].name, parameters[Index].value);
                }
            }
            const nodeToTransform = document.getElementById(nodeToTransformId);
            
            const transformedFragment = xslProc.transformToFragment(xmlDoc, document);
            const transformedDoc = xslProc.transformToDocument(xmlDoc);
            // Transform
            nodeToTransform.replaceChildren(transformedFragment);
        } else {
            // Browser unknown
            alert("Browser unknown");
        }
    } catch (e) {
        alert('Error: ' + e.message + ' Ref: runTransform');
    }
}

function menuTransform(xmlFileName, title) {
    try {
    var parameters = new Array();
    var parameter = new Object();
    parameter.name = 'XmlFileName';
    parameter.value = xmlFileName;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'Title';
    parameter.value = title;
    parameters.push(parameter);

    var nodeToTransform = 'MenuHeader';
    var xslFileName = 'FTOutput/XSL/menus.xsl';
    changeTitle(title);
    runTransform(window[xmlFileName], menusXSL, nodeToTransform, parameters);
    }
    catch (e) {
        alert('Error: ' + e.message + ' Ref: menuTransform');
    }
}

function warningsTransform(xmlFileName) {
    try {
    var parameters = new Array();
    var parameter = new Object();
    parameter.name = 'XmlFileName';
    parameter.value = xmlFileName;
    parameters.push(parameter);

    var nodeToTransform = 'ContentSpace';
    var xslFileName = 'FTOutput/XSL/warnings.xsl';
    clearNode('OverviewSpace');
    runTransform(FaultTrees, warningsXSL, nodeToTransform, parameters);
    }
    catch (e) {
        alert('Error: ' + e.message + ' Ref: warningsTransform');
    }
}

function topEventTransform(xmlFileName, ftName) {
    try {
    var parameters = new Array();
    var parameter = new Object();
    parameter.name = 'XmlFileName';
    parameter.value = xmlFileName;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'ftName';
    parameter.value = ftName;
    parameters.push(parameter);

    var nodeToTransform = 'OverviewSpace';
    
    runTransform(FaultTrees, topEventInfoXSL, nodeToTransform, parameters);
    }
    catch (e) {
        alert('Error: ' + e.message + ' Ref: topEventTransform');
    }
}

function cutSetsTransform(xmlFileName, ftName, sortType, sortOrder, PageSize, Page, cutSetOrder, basicEventID) {
    try {
    var parameters = new Array();
    var parameter = new Object();
    parameter.name = 'XmlFileName';
    parameter.value = xmlFileName;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'ftName';
    parameter.value = ftName;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'sortType';
    parameter.value = sortType;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'sortOrder';
    parameter.value = sortOrder;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'PageSize';
    parameter.value = PageSize;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'Page';
    parameter.value = Page;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'cutSetOrder';
    parameter.value = cutSetOrder;
    parameters.push(parameter);

    parameter = new Object();
    parameter.name = 'basicEventID';
    parameter.value = basicEventID;
    parameters.push(parameter);

    var nodeToTransform = 'ContentSpace';
    var xslFileName = 'FTOutput/XSL/cutsets.xsl';
    runTransform(window[xmlFileName], cutSetsXSL, nodeToTransform, parameters);
    }
    catch (e) {
        alert('Error: ' + e.message + ' Ref: cutSetsTransform');
    }
}

function optimisationSummaryTransform(xmlFileName) {
    try 
    {
    var parameters = new Array();
    var parameter = new Object();
    parameter.name = 'XmlFileName';
    parameter.value = xmlFileName;
    parameters.push(parameter);
    var nodeToTransform = 'OverviewSpace';
    var xslFileName = 'FTOutput/XSL/optimisationSummary.xsl';
    clearNode('OverviewSpace');
    runTransform(window[xmlFileName], optimisationSummaryXSL, nodeToTransform, parameters);
    }
    catch (e) {
    alert('Error: ' + e.message + ' Ref: optimisationSummaryTransform');
}
}

function optimisationTransform(xmlFileName, sortType, sortOrder) {
    try
    {
        var parameters = new Array();
        var parameter = new Object();
        parameter.name = 'XmlFileName';
        parameter.value = xmlFileName;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'sortType';
        parameter.value = sortType;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'sortOrder';
        parameter.value = sortOrder;
        parameters.push(parameter);
    
    
        var nodeToTransform = 'ContentSpace';
        var xslFileName = 'FTOutput/XSL/optimisation.xsl';
        runTransform(window[xmlFileName], optimisationXSL, nodeToTransform, parameters);
    }
    catch(e)
    {
        alert('Error: ' + e.message + ' Ref: optimisationTransform');
    }
}

function optimisationIndividualSummaryTransform(xmlFileName, individualID) {

    try
    {
        var parameters = new Array();
        var parameter = new Object();
        parameter.name = 'XmlFileName';
        parameter.value = xmlFileName;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'IndividualIDParam';
        parameter.value = individualID;
        parameters.push(parameter);
    
    
        var nodeToTransform = 'OverviewSpace';
        var xslFileName = 'FTOutput/XSL/optimisationSummary.xsl';
        runTransform(window[xmlFileName], optimisationSummaryXSL, nodeToTransform, parameters);
    }
    catch(e)
    {
        alert('Error: ' + e.message + ' Ref: optimisationIndividualSummaryTransform');
    }
}

function optimisationIndividualTransform(xmlFileName, encodingType, individualID) {

    try
    {
        var parameters = new Array();
        var parameter = new Object();
        parameter.name = 'XmlFileName';
        parameter.value = xmlFileName;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'IndividualIDParam';
        parameter.value = individualID;
        parameters.push(parameter);
    
    
        var nodeToTransform = 'ContentSpace';
        var xslFileName = encodingType + 'XSL';
        runTransform(window[xmlFileName], window[xslFileName], nodeToTransform, parameters);
    }
    catch(e)    
    {
        alert('Error: ' + e.message + ' Ref: optimisationIndividualTransform');
    }
}

function fmeaTransform(xmlFileName, FMEAType, Page, PageSize) {

    try
    {
        var parameters = new Array();
        var parameter = new Object();
        parameter.name = 'XmlFileName';
        parameter.value = xmlFileName;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'FMEAType';
        parameter.value = FMEAType;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'Page';
        parameter.value = Page;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'PageSize';
        parameter.value = PageSize;
        parameters.push(parameter);
    
        var nodeToTransform = 'ContentSpace';
        var xslFileName = 'FTOutput/XSL/FMEA.xsl';
        clearNode('OverviewSpace');
        runTransform(window[xmlFileName], fmeaXSL, nodeToTransform, parameters);
    }
    catch(e)
    {
        alert('Error: ' + e.message + ' Ref: fmeaTransform');
    }
}

function faultTreesTransform(xmlFileName, ftName) {

    try
    {
        var parameters = new Array();
        var parameter = new Object();
        parameter.name = 'XmlFileName';
        parameter.value = xmlFileName;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'ftName';
        parameter.value = ftName;
        parameters.push(parameter);
    
        var nodeToTransform = 'ContentSpace';
        var xslFileName = 'FTOutput/XSL/faultTreeView.xsl';
        runTransform(FaultTrees, faultTreeViewXSL, nodeToTransform, parameters);
    }
    catch(e)
    {
        alert('Error: ' + e.message + ' Ref: faultTreesTransform');
    }
}

function overviewTransform(xmlFileName, sortOrder) {

    try
    {
        var parameters = new Array();
        var parameter = new Object();
        parameter.name = 'XmlFileName';
        parameter.value = xmlFileName;
        parameters.push(parameter);
    
        parameter = new Object();
        parameter.name = 'sortOrder';
        parameter.value = sortOrder;
        parameters.push(parameter);
    
        var nodeToTransform = 'ContentSpace';
        var xslFileName = 'FTOutput/XSL/overviewTable.xsl';
        clearNode('OverviewSpace');
        runTransform(FaultTrees, overviewTableXSL, nodeToTransform, parameters);
    }
    catch(e)
    {
        alert('Error: ' + e.message + ' Ref: overviewTransform');
    }
}

function clearNode(nodeToClear) {
    try
    {
        if (document.implementation && document.implementation.createDocument) {
            // Mozilla
    
            //transform
            var node = document.getElementById(nodeToClear);
            while (node.hasChildNodes()) {
                node.removeChild(node.firstChild);
            }
        } else if (window.DOMParser || "DOMParser" in window) {
            // IE
    
    
            // Transform
            document.getElementById(nodeToClear).innerHTML = '';
        } else {
            // Browser unknown
            alert("Browser unknown");
        }
    }
    catch(e)
    {
        alert('Error: ' + e.message + ' Ref: clearNode');
    }
}