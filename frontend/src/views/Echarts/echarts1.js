export const kucun_echarts_data = (data) =>{

    var data_xAxis = [];
    var data_serios = [];
    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].goods_name);
        data_serios.push(data[i].total_quantity);
    }
    return {
        title: {
            text: '在庫レポート',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'商品名'
        },
        yAxis: {
            name:'棚卸コード数数量'
        },
        series: [
            {
                name: '在庫',
                type: 'bar',
                data: data_serios
            }
        ]
    }
}

export const caigou_echarts_data = (data) =>{

    var data_xAxis = [];
    var data_serios = [];
    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].goods_name);
        if(data[i].purchase_price!=null&&data[i].purchase_price!=undefined)
            data_serios.push(data[i].purchase_price);
        else
            data_serios.push(data[i].total_purchase_amount);
    }
    return {
        title: {
            text: '購買明細',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'商品名'
        },
        yAxis: {
            name:'購買価格'
        },
        series: [
            {
                name: '購買価格（円）',
                type: 'bar',
                data: data_serios
            }
        ]
    }
}


export const xiaoshou_echarts_data = (data) =>{

    var data_xAxis = [];
    var data_serios = [];
    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].goods_name);
        if(data[i].total_amount!=null&&data[i].total_amount!=undefined)
            data_serios.push(data[i].total_amount);
        else
            data_serios.push(data[i].total_sales_amount);
    }
    return {
        title: {
            text: '販売レポート',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'商品名'
        },
        yAxis: {
            name:'購買価格（円）'
        },
        series: [
            {
                name: '販売価格（円）',
                type: 'bar',
                data: data_serios
            }
        ]
    }
}


export const sales_predict_echarts = (data) =>{

    var data_xAxis = [];
    var data_serios_predict_price = [];
    var data_serios_predict_number = [];
    var data_serios_sales_price = [];
    var data_serios_sales_number = [];

    for(var i=0;i<data.length;i++){
        data_xAxis.push(data[i].name);
        data_serios_predict_price.push(data[i].predict_price);
        data_serios_predict_number.push(data[i].predict_number);

        data_serios_sales_price.push(data[i].sales_price);
        data_serios_sales_number.push(data[i].sales_quantity);
    }
    return {
        title: {
            text: 'データ比較',
            left:'center'
        },
        tooltip: {},
        xAxis: {
            data: data_xAxis,
            name:'商品名'
        },
        yAxis:{
            name:'予想価格（円）'
        }
        ,
        series: [
            {
                name: '予想価格（円）',
                type: 'bar',
                data: data_serios_predict_price
            },
            {
                name: '販売価格（円）',
                    type: 'bar',
                data: data_serios_sales_price
            },
            {
                name: '予想販売回数数数量',
                type: 'bar',
                data: data_serios_predict_number
            },
            {
                name: '販売回数数数量',
                type: 'bar',
                data: data_serios_sales_number
            }
        ]
    }
}


export const pie_echatrts = (data) =>{

    var echart_data = [];
    var temp = [];
    if(data.total_amount>data.collection_amount)
        temp = { value: data.total_amount-data.collection_amount, name: '支払いいいは受領されませんでした' };
    else
        temp = { value: data.collection_amount-data.total_amount, name: '支払いいいは受領されませんでした' };  
    echart_data.push({...temp});
    var temp = { value: data.collection_amount, name: '支払いいいを受け取りました' };
    echart_data.push({...temp});
    return   {
        title: {
            text: data.number,
            subtext:'データデータ統計',
            left: 'center'
          },
        tooltip: {
          trigger: 'item'
        },
        series: [
            {
              name: 'Access From',
              type: 'pie',
              radius: '50%',
              data: echart_data,
              emphasis: {
                itemStyle: {
                  shadowBlur: 5,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        // series: [
        //   {
        //     name: 'Access From',
        //     type: 'pie',
        //     radius: ['40%', '70%'],
        //     avoidLabelOverlap: false,
        //     itemStyle: {
        //       borderRadius: 10,
        //       borderColor: '#fff',
        //       borderWidth: 2
        //     },
        //     label: {
        //       show: false,
        //       position: 'center'
        //     },
        //     emphasis: {
        //       label: {
        //         show: true,
        //         fontSize: 12,
        //         fontWeight: 'bold'
        //       }
        //     },
        //     labelLine: {
        //       show: false
        //     },
        //     data: echart_data
        //   }
        // ]
      }
}

