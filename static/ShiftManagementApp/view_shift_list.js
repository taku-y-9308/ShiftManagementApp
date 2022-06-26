/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    axios
        .get('/shift-list-ajax/')
        .then((res)=>{
            console.log(res.data[0].date);
            let start_date = new Date(2022,6,1);
            let end_date = new Date(2022,6,30);
            let shift_list_date = document.getElementById('shift_list_date');
            let base_date = start_date;

            let tableEle = document.getElementById('data-table')
            for(let i=0;i<30;i++){
                let th = document.createElement('th');
                th.innerHTML = '2022/6/'+i;
                shift_list_date.appendChild(th);

                if(base_date == res.data[0].date)
                base_date.setDate(base_date.getDate()+1);
                console.log(base_date)

    
                
            }
            tableEle.appendChild(shift_list_date);
        })
        .catch((res)=>{
            console.log(res);
        })

}