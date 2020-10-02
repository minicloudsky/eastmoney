const cheerio = require("cheerio");
const axios = require("axios");
const express = require("express");
const app = express();
axios.default.defaults.headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    Referer: "http://fund.eastmoney.com",
    Host: "fund.eastmoney.com",
    'Cookie': 'em_hq_fls=js; qgqp_b_id=9715e29311d3fc5888ee05d9afbfcb92; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; waptgshowtime=2020917; st_si=25027075577965; ASP.NET_SessionId=t1vuewxy0cbz5wgyu2adoib5; HAList=a-sz-002127-%u5357%u6781%u7535%u5546%2Cd-hk-06862%2Ca-sz-000066-%u4E2D%u56FD%u957F%u57CE%2Cf-0-399006-%u521B%u4E1A%u677F%u6307; cowCookie=true; intellpositionL=1215.35px; st_asi=delete; intellpositionT=499.8px; searchbar_code=320007; EMFUND1=09-19%2013%3A04%3A14@%23%24%u9E4F%u626C%u5229%u6CA3%u77ED%u503AE@%23%24006831; EMFUND0=09-19%2001%3A35%3A46@%23%24%u5609%u5B9E%u589E%u957F%u6DF7%u5408@%23%24070002; EMFUND2=09-19%2013%3A42%3A08@%23%24%u519C%u94F6%u65B0%u80FD%u6E90%u4E3B%u9898@%23%24002190; EMFUND3=09-19%2016%3A40%3A24@%23%24%u94F6%u6CB3%u521B%u65B0%u6210%u957F%u6DF7%u5408@%23%24519674; EMFUND4=09-19%2016%3A50%3A54@%23%24%u4E2D%u878D%u4EA7%u4E1A%u5347%u7EA7%u6DF7%u5408@%23%24001701; EMFUND5=09-19%2022%3A34%3A36@%23%24%u5357%u534E%u745E%u626C%u7EAF%u503AC@%23%24005048; EMFUND6=09-19%2021%3A51%3A18@%23%24%u5DE5%u94F6%u65B0%u8D8B%u52BF%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408A@%23%24001716; EMFUND7=09-19%2022%3A36%3A19@%23%24%u534E%u5B89%u521B%u4E1A%u677F50%u6307%u6570%u5206%u7EA7B@%23%24150304; EMFUND9=09-20%2010%3A03%3A59@%23%24%u8BFA%u5B89%u6210%u957F%u6DF7%u5408@%23%24320007; EMFUND8=09-20 10:24:15@#$%u5B89%u4FE1%u6C11%u7A33%u589E%u957F%u6DF7%u5408C@%23%24008810; st_pvi=58947008966039; st_sp=2020-07-25%2000%3A32%3A56; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=294; st_psi=20200920102414487-0-3267835636',
};

function getFundRanking() {
    let date = new Date().toISOString().split('T')[0];
    let max_fund_num = 100000; // 基金最大个数
    let url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd="
        + date + "&ed=" + date + "&qdii=&pi=1&pn=" + max_fund_num + "&dx=1"
    console.log("getFundRanking url: " + url)
    return axios
        .get(url)
        .then(function (response) {
            let html_string = response.data.toString(); // 获取网页内容
            html_string += "rankData;";
            return Promise.resolve(eval(html_string));
        })
        .catch(function (error) {
            console.log(error);
        });
}

function getDiyFundRanking() {
    let end_date = new Date().toISOString().split('T')[0];
    let max_fund_num = 100000; // 基金最大个数
    let start_date = '1990-01-01';
    let url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=dy&dt=kf&ft=all&rs=&gs=0&sc=qjzf&st=desc&sd=" + start_date
        + "&ed=" + end_date + "&es=0&qdii=&pi=1&pn=" + max_fund_num + "&dx=0&v=" + Math.random()
    console.log("getDiyFundRanking url: " + url)
    return axios
        .get(url)
        .then(function (response) {
            let html_string = response.data.toString(); // 获取网页内容
            html_string += "rankData;";
            return Promise.resolve(eval(html_string));
        })
        .catch(function (error) {
            console.log(error);
        });
}

function getFundCompany() {
    let url = "http://fund.eastmoney.com/Data/FundRankScale.aspx?_=1600581086058"
    console.log("getFundCompany: " + url)
    return axios
        .get(url)
        .then(function (response) {
            let html_string = response.data.toString(); // 获取网页内容
            html_string += "\n json;";
            return Promise.resolve(eval(html_string));
        })
        .catch(function (error) {
            console.log(error);
        });
}

function getFbsFundRanking() {
    let url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=fb&ft=ct&rs=&gs=0&sc=zzf&st=desc&pi=1&pn=500000&v=0.027676829448198603"
    console.log("获取场内基金: " + url)
    return axios
        .get(url)
        .then(function (response) {
            let html_string = response.data.toString(); // 获取网页内容
            html_string += "\n rankData;";
            return Promise.resolve(eval(html_string));
        })
        .catch(function (error) {
            console.log(error);
        });
}

function getFundManager() {
    let page = 1
    let page_size = 100000
    let url = "http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn="
        + page_size + "&pi=" + page + "&sc=abbname&st=asc"
    console.log("获取基金经理: " + url)
    return axios
        .get(url)
        .then(function (response) {
            let html_string = response.data.toString(); // 获取网页内容
            html_string += "\n returnjson";
            return Promise.resolve(eval(html_string));
        })
        .catch(function (error) {
            console.log(error);
        });
}

app.get("/", (req, res) => {
    let type = req.query.type;
    if (type === 'fund_ranking') {
        let promise = getFundRanking(); // 发起抓取
        promise.then((response) => {
            res.json(response); // 数据返回
        });
    } else if (type === 'diy_fund_ranking') {
        let promise = getDiyFundRanking(); // 发起抓取
        promise.then((response) => {
            res.json(response); // 数据返回
        });
    } else if (type === 'fund_company') {
        let promise = getFundCompany(); // 发起抓取
        promise.then((response) => {
            res.json(response); // 数据返回
        });
    } else if (type === 'fbs_fund_ranking') {
        let promise = getFbsFundRanking(); // 发起抓取
        promise.then((response) => {
            res.json(response); // 数据返回
        });
    } else if (type === 'fund_manager') {
        let promise = getFundManager()
        promise.then((response) => {
            res.json(response); // 数据返回
        });
    }
});


app.listen(3000, () => console.log("Listening on port 3000!")); // 监听3000端口
