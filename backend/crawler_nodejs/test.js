const axios = require("axios");
const express = require("express");
const app = express();

axios.default.defaults.headers = {
    "Referer": "http://fund.eastmoney.com",
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

function getFundType(fund_type) {
    let page = 1
    let page_size = 100000
    let url = "https://fundapi.eastmoney.com/fundtradenew.aspx?ft="
        + fund_type + "&st=desc&pi=" + page + "&pn=" + page_size
    console.log("获取基金类型: " + url)
    return axios
        .get(url)
        .then(function (response) {
            let html_string = response.data.toString(); // 获取网页内容
            html_string += "\n rankData";
            return Promise.resolve(eval(html_string));
        })
        .catch(function (error) {
            console.log(error);
        });
}

app.get("/", (req, res) => {
    let type = req.query.type;
    let fund_type = req.query.fund_type;
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
    } else if (type === 'fund_type') {
        let promise = getFundType(fund_type)
        promise.then((response) => {
            res.json(response); // 数据返回
        });
    }
});


app.listen(3000, () => console.log("Listening on port 3000!")); // 监听3000端口
