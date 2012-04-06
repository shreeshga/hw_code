import java.io.BufferedWriter;
//import java.io.File;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.ListIterator;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.TreeMap;

public class Main {

	/**
	 * @param args
	 * @throws IOException 
	 */
	
	public static String PATH = "";
	public static HashMap shingleList = new HashMap();
	public static HashMap randomPairs = new HashMap();
	public static TreeMap documents= new TreeMap();
	public static TreeMap documentsSketch= new TreeMap();
	public static int i = 0;
	public static int p;
	
	public static void randomPairGenerator()
	{
		Random r = new Random();
		int as = r.nextInt(p-1) + 1;
		int bs = r.nextInt(p);
		for (int k = 0; k < 25; k++){
			bs = r.nextInt(p);
			while(randomPairs.containsKey(as)){
				// as has to be between 1 and p-1
				as = r.nextInt(p-1) + 1;
			}
			randomPairs.put(as, bs);
		}
		
		Set keys = randomPairs.keySet(); //set of ranks
        Iterator it = keys.iterator();
        int count = 1;
        while(it.hasNext()){
            //System.out.println(count++);
        	as = (Integer)it.next();
            bs = (Integer)randomPairs.get(as);
            //System.out.println("as : " + as + " bs : " + bs);

        }
	}
	public static void generateSketch(int docId){
		// for each of the 25 random numbers pairs as,br do : ((as*x) + bs)mod p
		Set keys = randomPairs.keySet(); //set of ranks
		LinkedList sketchList = new LinkedList();
        Iterator it = keys.iterator();
        int smallest;
        
        while(it.hasNext()){
        	smallest = 1000000000;
        	int as = (Integer)it.next();
            int bs = (Integer)randomPairs.get(as);
            //function 1
            //apply function 1 to all the x's of a doc
            //get all shungles of a doc
    		LinkedList shingleList =(LinkedList) documents.get(docId); 
    		ListIterator li= shingleList.listIterator();
            while(li.hasNext()){
            	int x = (Integer)li.next();
                int y = (((as*x) + bs)%p);
                if(y < smallest){
                	smallest = y;
                }
           }
           sketchList.add(smallest);
        }
        //System.out.println(sketchList.size());
        documentsSketch.put(docId, sketchList);
	}
	
	public static void populateSketch(){
		//for each doc generate sketch
		for(int j = 0 ; j <= 99; j++ ){
			generateSketch(j);
		}
		
		 Set keys = documentsSketch.keySet(); //set of ranks
         Iterator it = keys.iterator();
         int i =0;
         while(it.hasNext()){
        	 System.out.println("\nDocument " + i);
             LinkedList shingleList =(LinkedList) documentsSketch.get(it.next());
             ListIterator li= shingleList.listIterator();
             while(li.hasNext()){
                //get snippet for these docs
                int shingleId = (Integer)li.next();
                //access URL and get content=title + first few words
                System.out.print(shingleId + " ");
                
             }
             i++;
         }
	}
	
	public static void calculateJaccardexact(int d1, int d2)
	{
		LinkedList d1List =(LinkedList) documents.get(d1); 
		LinkedList d2List =(LinkedList) documents.get(d2); 
		
		
		int total = d1List.size() + d2List.size();
		
		//d1List will have intersection
		d1List.retainAll(d2List);
		// intersection quantity
		double intersection = d1List.size();
		//union is total minus intersection
		double union = total - intersection;
		System.out.println("Actual Jaccard ");
		System.out.println("Documents " + d1 + " " + d2 + "  Jaccard = " + (intersection/union));
		System.out.println();
	}
	public static void calculateJaccardapprox()
	{
		Integer[][] dMat = new Integer[100][25];
		Integer[] tempArr = new Integer[25];
		int docid = 0;
        
	    Set keys = documentsSketch.keySet(); //set of ranks
	    Iterator it = keys.iterator();
	    //for each document
	    while(it.hasNext()){
	    	
	    	LinkedList<Integer> sketchList =(LinkedList) documentsSketch.get(it.next());
	    	sketchList.toArray(tempArr);
	    	for(int s = 0 ; s<25; s++){
	    		//System.out.println("***" + tempArr[s]);
	    		dMat[docid][s] = tempArr[s];
	    	}
	    	docid++;
	    }
	    System.out.println();
	    System.out.println("---------------------------------");
	    System.out.println("Jaccard Calculation");
	    System.out.println("---------------------------------");
	    int k = 0;
	    for(int d1 = 0 ; d1 <= 99; d1++){
	    	for(int d2 = (d1+1); d2 <= 99; d2++)
	    	{
	    		k = 0;
	    		for(int s = 0 ; s<25; s++)
	    		{
	    			if(dMat[d1][s] == dMat[d2][s])
	    			{
	    				//System.out.println(dMat[d1][s] + "    " + dMat[d2][s]);
	    				k++;
	    			}
	    			
	    		}
	    		//System.out.println(k + "***" + k/25);
	    		if((k/25.0) > 0.5){
	    			System.out.println("Estimated Jaccard ");
	    			System.out.println("Documents " + d1 + " " + d2 + "  Jaccard = " + (k/25.0));
	    			calculateJaccardexact(d1, d2);
	    		}
	    	}
	    }
	}
	public static void calculateJaccardneighbors()
	{
		Integer[][] dMat = new Integer[100][25];
		Integer[] tempArr = new Integer[25];
		int docid = 0;
        
	    Set keys = documentsSketch.keySet(); //set of ranks
	    Iterator it = keys.iterator();
	    //for each document
	    while(it.hasNext()){
	    	
	    	LinkedList<Integer> sketchList =(LinkedList) documentsSketch.get(it.next());
	    	sketchList.toArray(tempArr);
	    	for(int s = 0 ; s<25; s++){
	    		//System.out.println("***" + tempArr[s]);
	    		dMat[docid][s] = tempArr[s];
	    	}
	    	docid++;
	    }
	    System.out.println();
	    System.out.println("---------------------------------");
	    System.out.println("Nearest Neighbors");
	    System.out.println("---------------------------------");
	    int k = 0;
	    for(int d1 = 0 ; d1 <= 9; d1++){
	    	for(int d2 = 0; d2 <= 99; d2++)
	    	{
	    		if (d1==d2)
	    			break;
	    		k = 0;
	    		for(int s = 0 ; s<25; s++)
	    		{
	    			if(dMat[d1][s] == dMat[d2][s])
	    			{
	    				//System.out.println(dMat[d1][s] + "    " + dMat[d2][s]);
	    				k++;
	    			}
	    			
	    		}
	    		//System.out.println(k + "***" + k/25);
	    		TreeMap tempMap= new TreeMap();
	    		
	    		if((k/25.0) > 0.5){
	    			System.out.println("Estimated Jaccard ");
	    			System.out.println("Documents " + d1 + " " + d2 + "  Jaccard = " + (k/25.0));
	    			calculateJaccardexact(d1, d2);
	    		}
	    	}
	    }
	}
	public static void parseDocument(String fileName, int docId)
	{
		try {
			//System.out.println("dociddddd             " +  docId);
			String filePath = PATH + fileName;
		    LinkedList shingleSet = new LinkedList();
			File file = new File(filePath);
			StringBuilder builder = new StringBuilder();
		
			Scanner scanner = new Scanner(file);
			String word = "";
			
			while(scanner.hasNext()){
				word = scanner.next();
				builder.append(word);
				builder.append(" ");
			}
			
			StringTokenizer st = new StringTokenizer(builder.toString());
			String first = st.nextToken();
			String second = st.nextToken();
			String third = "";
			String shingle = "";
			
			while(st.hasMoreTokens()){
				third = st.nextToken();
				shingle = first + "," + second + "," + "" + third;
				//insert shingle

				if(!shingleList.containsKey(shingle)){
					shingleList.put(shingle, i);
					shingleSet.add(i);
					i++;
				}else{
					if(!shingleSet.contains(i)){
						shingleSet.add(shingleList.get(shingle));
					}
					
				}
				
				//System.out.println(shingle);
				first = second;
				second = third;
			}
			
			documents.put(docId, shingleSet);
			/*Iterator iterator = shingleList.keySet().iterator();  
			   
			while (iterator.hasNext()) {  
			   String key = iterator.next().toString();  
			   String value = shingleList.get(key).toString();  
			   
			   System.out.println(key + " " + value);  
			}
			//System.out.println(shingleList.toString());
			 Set keys1 = documents.keySet(); //set of ranks
	         Iterator it1 = keys1.iterator();
	         int np =0;
	         while(it1.hasNext()){
	        	 System.out.println("\nDocument " + np);
	             LinkedList shingles =(LinkedList) documents.get(it1.next());
	             ListIterator li1= shingles.listIterator();
	             while(li1.hasNext()){
	                //get snippet for these docs
	                int shingleId = (Integer)li1.next();
	                //access URL and get content=title + first few words
	                System.out.print(shingleId + " ");			
	             }
	            np++;
	         }*/
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	public static void calculateNearestNeighbors()
	{
		Integer[][] dMat = new Integer[100][25];
		Integer[] tempArr = new Integer[25];
		int docid = 0;
        TreeMap temp = new TreeMap();
	    Set keys = documentsSketch.keySet(); //set of ranks
	    Iterator it = keys.iterator();
	    //for each document
	    while(it.hasNext()){
	    	
	    	LinkedList<Integer> sketchList =(LinkedList) documentsSketch.get(it.next());
	    	sketchList.toArray(tempArr);
	    	for(int s = 0 ; s<25; s++){
	    		//System.out.println("***" + tempArr[s]);
	    		dMat[docid][s] = tempArr[s];
	    	}
	    	docid++;
	    }
	    System.out.println();
	    System.out.println("---------------------------------");
	    System.out.println("Nearest Neighbors");
	    System.out.println("---------------------------------");
	    int k = 0;
	    for(int d1 = 0 ; d1 <= 9; d1++)
	    {
	    	for(int d2 = 0; d2 <= 99; d2++)
	    	{
	    		if(d1 == d2){
	    			continue;
	    		}
	    		k = 0;
	    		for(int s = 0 ; s<25; s++)
	    		{
	    			if(dMat[d1][s] == dMat[d2][s])
	    			{
	    				//System.out.println(dMat[d1][s] + "  0000000000000000000000000000000000  " + dMat[d2][s]);
	    				k++;
	    			}
	    			
	    		}
	    		//System.out.println(k + "***" + k/25);
	    		temp.put((k/25.0), d2);
	    	}
	    	   	
			Set keyset = temp.descendingKeySet();
	        Iterator itr = keyset.iterator();
	        int counter = 0;
	        while(itr.hasNext() && counter < 3){
	        	counter++;
	        	Double jc = (Double)itr.next();
	            Integer doc = (Integer)temp.get(jc);
	            System.out.println("Document " + d1 + " Neighbor:" + counter + " is  " + doc + "  with Jaccard Coeff  "  + jc);
	            
	        }
	        System.out.println();
	    	
	    }
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
	    if(args.length < 1){
            System.out.println("try: java -jar minHash.jar <path of test folder>");
            System.exit(0);
        }
	    else{
	    	PATH = args[0];
	    }
		for(int j = 0 ; j <= 99; j++ )
		{
			if(j <=9){
				parseDocument("file0" + j + ".txt", j);
			}else{
				parseDocument("file" + j + ".txt", j);
			}
		}
		p= shingleList.size();
		System.out.println("P= " + shingleList.size());
		randomPairGenerator();
		populateSketch();
		
		calculateJaccardapprox();
		calculateNearestNeighbors();
	}

}