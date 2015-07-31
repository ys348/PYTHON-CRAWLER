var json_testing;
var node_str='';
var url_sum_total=0;
var node_plaintext='';
var tid;

String.prototype.times = function(n) {
    return Array.prototype.join.call({length:n+1}, this);
};
			
function urlGo(){
	//alert($("#url_input").val());
	$('#go_button').css('display','none');
	$('#refresh_button').css('display','inline');
	$('#refresh_text').css('visibility','visible');
	


	var crawler_mode=$( "input:checked" ).val();

	if($('#status').text()==''){
		
		var query_url=$("#url_input").val();
		
		if(query_url==''){
			$('#go_button').css('display','inline');
			$('#refresh_button').css('display','none');
			$('#refresh_text').css('visibility','hidden');
			alert('URL can not be empty!');

			return;
		};
		
		$.ajax({
			type: "POST",
			url: "/urlgo/",
			dataType: 'text',
			data: "url="+$("#url_input").val()+"&mode="+crawler_mode,
			beforeSend:function(){
				$('#status').css('visibility','visible');
				$('#status').text('pre-calculating... (in average, it takes 1 minute)');
				tid=setInterval('status_tracking()',1500);
				//alert($('#status').text());
			},
			success:function(data){
				//alert(data);
				//$('#status').text('complete!');
				//$('#tree_loading').css('display','inline');
				clearTimeout(tid);
				
				node_str='';
				node_plaintext=''
				
				try{
					json_testing=JSON.parse(data);
				}catch(e){
				alert(data);  // if data is not a valid json array, which means it's the error msg
				//alert('Some unexpected error just happended, I\'m so sorry for that... Try something else please ');
				//location.reload();
				return;
				}
				$('#status').text('creating structure tree...');
				url_sum_total=json_testing['url_sum_total'];
				TLD_value=json_testing['TLD_value'];
				
				if(jQuery.isEmptyObject(json_testing['root_nodes'])){
					alert('Oops, the URL you just entered is unaccessible :(');
					clearTimeout(tid);
					$('#status').text('');
					//$("#url_input").val('');
					var text_input = document.getElementById ('url_input');
					text_input.focus ();
					text_input.select ();
					
					$('#go_button').css('display','inline');
					$('#refresh_button').css('display','none');
					$('#refresh_text').css('visibility','hidden');
					return;
				}
				
				node_plaintext=TLD_value+'\t\t'+get_current_data_time()+'\r\n';
				
				recersive_node('root_nodes',1);
				$('#status').text('');
				$nodeTree="<div style='margin-top:20px;margin-bottom:50px;'>"+
				"<div class='row'>"+
				  "<span id='copy_comment' class='col-lg-6 col-md-6 col-sm-6 col-xs-sm-6' onclick='copy_to_clipboard()'"+
				    "style='cursor:pointer;color:#a8a8a8;font-weight:bold;margin-left:20px;margin-bottom:-6px;'>"+
					"Copy to Clipboard</span>"+
				  "<span id='textarea_comment' class='col-lg-6 col-md-6 col-sm-6 col-xs-sm-6'"+
				    "style='font-weight:bold;margin-left:20px;margin-bottom:6px;display: none;'>"+
					"press CTRL+C in Windows or Command+C in Mac"+
					    "<span onclick='back_from_textarea()' style='cursor:pointer;color:#a8a8a8;'>"+
						"  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Go back</span>"+
				  "</span>"+
				"</div>"+
				"<table id='example-advanced' style='width:100%;'>"+
				"<tr>"+
				"<td>The following structure is based on<span style='font-style:italic;'>"+url_sum_total+"</span> URLs from "+TLD_value+" <span style='font-size:12px;font-weight:bold;color:red;'>"+get_current_data_time()+"</span></td>"+
				"</tr>"+
				"<tr data-tt-id='root_nodes' >"+
				'<td>'+TLD_value+'</td>'+
				"</tr>"+node_str+
				"</table>"+
				"<textarea rows='50' style='width:100%;display: none;' id='text_area'>"+
				node_plaintext+
				"</textarea></div>";		
				
				$('#URL_input_box').after($nodeTree);

				$("#example-advanced").treetable({ expandable: true,clickableNodeNames: true,initialState:'collapsed',indent:'100'});

				$('#status').text('');

				$('#go_button').css('display','inline');
				$('#refresh_button').css('display','none');
				$('#refresh_text').css('visibility','hidden');
				//$('#tree_loading').css('display','none');
			}
		});
		
		
	}else{

	};


};

function terminate_query(){
	
			$.ajax({
			type: "POST",
			url: "/urlReTry/",
			dataType: 'text',
			beforeSend:function(){
				clearTimeout(tid);
				$('#status').text('terminating...');
				//alert($('#status').text());
			},
			success:function(data){
				
				$('#status').text('');
				$('#go_button').css('display','inline');
				$('#refresh_button').css('display','none');
				$('#refresh_text').css('visibility','hidden');
				alert('current process has been terminated!');
				location.reload();
				//var text_input = document.getElementById ('url_input');
				//text_input.focus ();
				//text_input.select ();
			}
			
		});
	//location.reload();
};

function copy_to_clipboard(){
	$('#copy_comment').css('display','none');
	$('#example-advanced').css('display','none');
	$('#textarea_comment').css('display','inline');
	$('#text_area').css('display','inline');

	var text_area = document.getElementById ('text_area');
	text_area.focus ();
	text_area.select ();
	
};

function back_from_textarea(){
	
	$('#textarea_comment').css('display','none');
	$('#text_area').css('display','none');
	$('#copy_comment').css('display','inline');
	$('#example-advanced').css('display','inline');
};


function status_tracking(){
	
	$.ajax({
        type: "POST",
        url: "/urltracing/",
        dataType: 'text',
        data: "request=tracking",
		success:function(data){
			if(data==''){
				
			}
			$('#status').text(data);
			
			if (data=='pre-calculating... (in average, it takes 1 minute)'){
				setTimeout(function(){$('#status').text('pre-calculating..  (in average, it takes 1 minute)');},500);
				setTimeout(function(){$('#status').text('pre-calculating.   (in average, it takes 1 minute)');},1000);
			}else if(data=='terminating current query...'){
				
			}
						
		}
        });
	
};

function get_nodes_perct(num_nodes){
	var nodes_perct=(num_nodes*100/url_sum_total).toFixed(2);
	if (nodes_perct<0.5){
		nodes_perct='<0.5';
	}
return '('+nodes_perct+'%)';
	
}

function testing_func(json_data){  		// return a 2d array from json data
	keys=Object.keys(json_data);		// the first d is the num, the second d is the node name
	var values=[];
	for (var i=0;i< keys.length;i++){
		values[i]=json_data[keys[i]]

	}
	var nodes=[];
	nodes[0]=values;
	nodes[1]=keys;
	return nodes
}


function get_sorted_array(array){		// return a sorted 2d array, each sub array is the num and ndoe

	var copy_array=array;
	array_length=array[0].length;
	var sorted_array=new Array(array_length);
	for (var i=0;i<array_length;i++){
		sorted_array[i]=new Array(2);
	}

	for (var i=0;i<copy_array[0].length;i++){

		sorted_array[i][0]=Math.max.apply(null, copy_array[0]);  //put the max value here
		var array_index=copy_array[0].indexOf(Math.max.apply(null, copy_array[0]));   // keep the index
		copy_array[0][array_index]=-100; //reset the value to a very small one
		sorted_array[i][1]=copy_array[1][array_index];   //put the corresponding key name here

	}
	return sorted_array;
}

var myArray=new Array();

function recersive_node(target_node,n){

	if (json_testing.hasOwnProperty(target_node)){
		 myArray[target_node]=[];
		node_array=get_sorted_array(testing_func(json_testing[target_node]));
		myArray[target_node][0]=node_array;
		for(myArray[target_node][1]=0;myArray[target_node][1]<myArray[target_node][0].length;myArray[target_node][1]=myArray[target_node][1]+1){
			var target_node_2=myArray[target_node][0][myArray[target_node][1]][1];
			var node_percentage=get_nodes_perct(myArray[target_node][0][myArray[target_node][1]][0]);
			node_plaintext=node_plaintext+'\t'.times(n)+target_node_2+' '+node_percentage+'\r\n';
			node_str=node_str+"<tr data-tt-id='"+myArray[target_node][0][myArray[target_node][1]][1]+"' data-tt-parent-id='"+target_node+"'>"+
				'<td>'+target_node_2+' '+node_percentage+'</td>'+
				'</tr>';
			recersive_node(myArray[target_node][0][myArray[target_node][1]][1],n+2);

		}
		return;
	}else{

		
		return ;
	}

}

function get_current_data_time(){
	
			var currentdate = new Date(); 
			var monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

			var month=monthNames[currentdate.getMonth()];
			var sec=currentdate.getSeconds();
			if (sec<10){
				sec='0'+sec;
			}
			var minutes=currentdate.getMinutes();
			if (minutes<10){
				minutes='0'+minutes;
			}
			var datetime = month+ " "
                +  currentdate.getDate() + ", " 
                + currentdate.getFullYear() + "  at "  
                + currentdate.getHours() + ":"  
                + minutes + ":" 
                + sec;
			return datetime;
}
//alert(json_testing.hasOwnProperty('root_nodess'));

//recersive_node('root_nodes');
