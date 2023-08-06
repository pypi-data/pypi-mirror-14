
import abner.*;

import java.io.*;
import java.lang.*;
import java.util.*;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import org.w3c.dom.Node;
import org.w3c.dom.Element;


public class Tagging {

	private static String[][] allAbstracts;
	private static String[][] allTitles;
	private static String[][] allPmids;
	private static int n;
	private static String input_path;
	private static String output_path;
    public static void main(String[] args)  {
 		
 		input_path = args[0];
 		output_path = args[1];
   		File folder = new File(input_path);
		File[] listOfFiles = folder.listFiles();
		n = listOfFiles.length - 1;
		System.out.println(n);
    	allAbstracts = new String[n][];
    	allTitles = new String[n][];
    	allPmids = new String[n][];
    	try {
			parse();
		} catch (SAXException | IOException | ParserConfigurationException e) {
			e.printStackTrace();
		}
    	
    	try {
			save();
		} catch (TransformerException e) {
			e.printStackTrace();
		}
    
    }	
 
    //tagging abstracts and titles and store them with associated pmid in 3 2-D arrays   
    public static void parse() throws SAXException, IOException, ParserConfigurationException{
    	Tagger t = new Tagger();
    	 //numbers of files 
    	DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
    	DocumentBuilder dBuilder = dbFactory.newDocumentBuilder(); 	
    	File folder = new File(input_path);
		File[] listOfFiles = folder.listFiles();
    	for (int i = 0; i < n; i++){
    		Document doc = dBuilder.parse(new File(listOfFiles[i+1].getPath()));
    		doc.getDocumentElement().normalize();
    		System.out.println(i+"th block######################################");
    		// System.out.println("Root element :" + doc.getDocumentElement().getNodeName());
	    	NodeList nList=doc.getElementsByTagName("PubMedArticle");
	    	String[] abstracts = new String[nList.getLength()];
	    	String[] titles = new String[nList.getLength()];
	    	String[] pmids = new String[nList.getLength()];
	    	String articleAbstract = new String();
	    	String articleTitle = new String();
	    	String pmid = new String();
	    	for (int j = 0; j < nList.getLength(); j++) {
	    		Node nNode = nList.item(j);
	    		// System.out.println(j+"th article#################################");
	    		// System.out.println("\nCurrent Element :" + nNode.getNodeName());
	    		if (nNode.getNodeType() == Node.ELEMENT_NODE) {
	    			Element eElement = (Element) nNode;
	    			pmid=eElement.getElementsByTagName("PMID").item(0).getTextContent();
	    			pmids[j]=pmid;
	    			articleTitle= eElement.getElementsByTagName("Title").item(0).getTextContent();	
	    			//in case some articles don't have an abstract, if no abstract, store "none" in array
	    			if(eElement.getElementsByTagName("Abstract").item(0)!=null){
	    				articleAbstract= eElement.getElementsByTagName("Abstract").item(0).getTextContent();
	    			}else{
	    				articleAbstract="none";	    				
	    			}
	    			//tag title and abstract
	    			articleAbstract=t.tagSGML(articleAbstract);
		    		articleTitle=t.tagSGML(articleTitle);
		    		//keep sentences contains protein or DNA of title
		    		if(articleTitle.contains("<PROTEIN>") || articleTitle.contains("<DNA>")){
		    			String newTitle = ((String) articleTitle.subSequence(0, articleTitle.length()-3));
		    			newTitle =newTitle.replaceAll("<PROTEIN>", "");
		    			newTitle =newTitle.replaceAll("</PROTEIN>", "");
		    			newTitle =newTitle.replaceAll("<DNA>", "");		    			
		    			newTitle =newTitle.replaceAll("</DNA>", "");
		    			newTitle =newTitle.replaceAll("<CELL_TYPE>", "");		    			
		    			newTitle =newTitle.replaceAll("</CELL_TYPE>", "");
		    			newTitle =newTitle.replaceAll("<RNA>", "");		    			
		    			newTitle =newTitle.replaceAll("</RNA>", "");
		    			newTitle =newTitle.replaceAll("<CELL_LINE>", "");		    			
		    			newTitle =newTitle.replaceAll("</CELL_LINE>", "");
		    			titles[j]=newTitle;
					}else{
						titles[j]="none";
					}		    		
		    		//keep sentences contains protein or DNA of abstracts
		    		String newAbstract="";
	    			if(articleAbstract=="none"){
	    				continue;
	    			}else{
	    				String[] temp = articleAbstract.split("\n");
	    				for(int r=0;r<temp.length;r++){
	    					if(temp[r].contains("<PROTEIN>") || temp[r].contains("<DNA>")){
	    						newAbstract=newAbstract+temp[r]+"\n";
	    						newAbstract =newAbstract.replaceAll("<PROTEIN>", "");
	    						newAbstract =newAbstract.replaceAll("</PROTEIN>", "");
	    						newAbstract =newAbstract.replaceAll("<DNA>", "");		    			
	    						newAbstract =newAbstract.replaceAll("</DNA>", "");
	    						newAbstract =newAbstract.replaceAll("<CELL_TYPE>", "");		    			
	    						newAbstract =newAbstract.replaceAll("</CELL_TYPE>", "");
	    						newAbstract =newAbstract.replaceAll("<RNA>", "");		    			
	    						newAbstract =newAbstract.replaceAll("</RNA>", "");
	    						newAbstract =newAbstract.replaceAll("<CELL_LINE>", "");		    			
	    						newAbstract =newAbstract.replaceAll("</CELL_LINE>", "");
	    					}
	        			}
	    			}
	    			abstracts[j]=newAbstract;
	    			// System.out.println(j+"th article#################################");
	    			// System.out.println(pmids[j]);
	    			// System.out.println(titles[j]);
	    			// System.out.println(abstracts[j]);
	    			// System.out.println();
	    		}
	    	allPmids[i]=pmids;
	    	allAbstracts[i]=abstracts;
	    	allTitles[i]=titles;
	    	}	    	
    	}
    }
    
    //access pmids,abstracts,titles by index and write them in a new xml.file
    public static void save() throws TransformerException{
        try {
        	DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
    		DocumentBuilder docBuilder = docFactory.newDocumentBuilder();
    		// root elements
    		Document newdoc = docBuilder.newDocument();
    		Element rootElement = newdoc.createElement("PubMedArticleSet");
    		newdoc.appendChild(rootElement);
        	for(int m=0;m<n;m++){
	    		String[] tempPmids = allPmids[m];
	    		System.out.print(tempPmids);
	    		String[] tempTitles = allTitles[m];
	    		String[] tempAbstracts = allAbstracts[m];
	    		System.out.println(m+"th block####################");
	    		for(int k=0; k<tempPmids.length; k++){
	    			Element pubmedArticle = newdoc.createElement("PubMedArticle");
	        		rootElement.appendChild(pubmedArticle);
	    			String id = tempPmids[k];
	    			String tit = tempTitles[k];
	    			String abs = tempAbstracts[k];
	    			//pmid
	    			Element pubmedID = newdoc.createElement("PMID");
	    			pubmedID.appendChild(newdoc.createTextNode(id));
	    			pubmedArticle.appendChild(pubmedID);
	    			//title
	    			if(tit!="none"){
		    			Element pubmedTitle = newdoc.createElement("Title");
		    			pubmedTitle.appendChild(newdoc.createTextNode(tit));
		    			pubmedArticle.appendChild(pubmedTitle);
	    			}
	    			//abstract
	    			if(abs=="none"){
	    				
	    			}else{
	    				String[] temp = abs.split("\n");
	    				Element pubmedAbstract= newdoc.createElement("Abstract");
	    				for(int r=0;r<temp.length;r++){	    			
	    					pubmedAbstract.appendChild(newdoc.createTextNode(temp[r]));
	    				}
	    				pubmedArticle.appendChild(pubmedAbstract);
	    			}
	    		}
	    	}
        	// write the content into xml file       	
    		TransformerFactory transformerFactory = TransformerFactory.newInstance();
    		Transformer transformer = transformerFactory.newTransformer();
    		transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        	transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
    		DOMSource source = new DOMSource(newdoc);  
    		//change the pathname when using it, the created xml file will be stored in this path
    		StreamResult result = new StreamResult(new File(output_path));
    		transformer.transform(source, result);
    		System.out.println("File saved!");
        } catch (ParserConfigurationException pce) {
    		pce.printStackTrace();
        }
    }    
}
        
    



