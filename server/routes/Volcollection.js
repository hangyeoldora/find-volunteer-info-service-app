const express = require("express");
const router = express.Router();
const request = require("request");


router.get("/", async (req, res) =>{

    const seachItem = req.params.seachItem;
    let url = "http://apis.data.go.kr/B460014/vmsdataview/getCenterList";
    
    let queryParams = 
    "?" + "serviceKey=" + "0lTocdsXSK4obDQqjM5QfIYgSGNTpOtc49pCGQx5pOr117fzHkizqB9v34zX%2BniOyJx%2Fs7oaBPFV48bJnjJhBg%3D%3D";
    queryParams += 
    "&" + "numOfRows=" + encodeURIComponent("20");
    queryParams +=
    "&"  + "pageNo=" + encodeURIComponent("1");
    queryParams +=
    "&"  + "areaCode=" + encodeURIComponent("0101");

    request(
        {
            url: url + queryParams,
            method: "GET",
        },
        (error, response, body) => {
            res.send(JSON.stringify(body));
            

        }
    );
});

module.exports = router;