
console.log('jjjjjjjjjjjjjjjjjjj')
let btn=document.getElementById('test')
btn.addEventListener('click',buttonClickHandler)
       function buttonClickHandler() {
            	// body...
            	console.log('hey');
            	const xhr=new XMLHttpRequest();
            	xhr.open('GET','/testing',true);
            	xhr.onprogress=function(){
            		console.log('hello')
            	}

            	xhr.onload=function(){
            		console.log(this.responseText)
            	}
            }     
            