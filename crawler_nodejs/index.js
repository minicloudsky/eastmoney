const cheerio = require("cheerio");
const axios = require("axios");
const express = require("express");
const app = express();
axios.default.defaults.headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    Referer: "http://fund.eastmoney.com/data/diyfundranking.html",
    Host: "fund.eastmoney.com",
};

function getFundRanking() {
    let date = new Date().toISOString().split('T')[0];
    let max_fund_num = 100000; // 基金最大个数
    let url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd="
        + date + "&ed=" + date + "&qdii=&pi=1&pn=" + max_fund_num + "&dx=1"
    console.log("get url: " + url)
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
    console.log("get url: " + url)
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
    }
});

app.get("/:time-:language", (req, res) => {
    const {
        time, // 获取排序时间
        language, // 获取对应语言
    } = req.params;
    let promise = getData(time, language); // 发起抓取
    promise.then((response) => {
        res.json(response); // 数据返回
    });
});

app.get("/:time", (req, res) => {
    const {
        time, // 获取排序时间
    } = req.params;
    let promise = getData(time); // 发起抓取
    promise.then((response) => {
        res.json(response); // 数据返回
    });
});

app.listen(3000, () => console.log("Listening on port 3000!")); // 监听3000端口
