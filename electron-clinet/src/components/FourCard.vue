<template>
    <div class="container-top">
        <div class="box">
            <div class="header">
                <div><b>用户增量</b></div>
                <div></div>
                <div class="sub-box" id="week">年/人</div>
            </div>
            <div class="content">2600</div>
            <div class="footer">
                <div class="total">总用户数</div>
                <div>35000</div>
            </div>
        </div>
		<div class="box">
            <div class="header">
                <div><b>访问次数</b></div>
                <div></div>
                <div class="sub-box" id="year">月/次</div>
            </div>
            <div class="content">2800</div>
            <div class="footer">
                <div class="total">总访问次数</div>
                <div>118000</div>
            </div>
        </div>
        <div class="box">
            <div class="header">
                <div><b>群组增量</b></div>
                <div></div>
                <div class="sub-box" id="day">月/个</div>
            </div>
            <div class="content">260</div>
            <div class="footer">
                <div class="total">总群组数量</div>
                <div>5800</div>
            </div>
        </div>
		<div class="box">
            <div class="header">
                <div><b>上传次数</b></div>
                <div></div>
                <div class="sub-box" id="week">月/次</div>
            </div>
            <div class="content">48000</div>
            <div class="footer">
                <div class="total">总上传次数</div>
                <div>463000</div>
            </div>
        </div>
    </div>
</template>

<script>

</script>

<style scoped>
.container-top {
	display: flex;
	justify-content: space-between;
	width: 90%;
	margin: 25px auto;
}

.box {
	width: 23%;
	height: 160px;
	background-color: #fbfbfb;
	border-radius: 10px;
	padding: 10px;
	box-sizing: border-box;
}

.header,
.footer {
	display: flex;
	align-items: center;
	height: 20%;
}

.header {
	margin-bottom: 5px;
	justify-content: space-between;
}

.footer {
	justify-content: space-around;
}

.header>div:nth-child(1) {
	flex-grow: 2;
}

.header>div:nth-child(2) {
	flex-grow: 3;
}

.header>div:nth-child(3) {
	flex-grow: 2;
}

.content {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 60%;
	font-size: 24px;
	font-weight: bold;

	border-top: 1px solid #000;
	/* 设置上边框 */
	/* border-bottom: 1px solid #000; 设置下边框 */
	/* padding: 5px; 内边距 */
}

.header div,
.footer div {
	/* flex: 1; */
	display: flex;
	align-items: center;
}

.sub-box {
	width: 10px;
	height: 20px;
	border-radius: 5px;
	display: flex;
	justify-content: center;
	align-items: center;
}

#year {
	background-color: rgb(246, 255, 237);
	border: 1px solid rgb(183, 235, 143);
	color: rgb(56, 185, 13);
}

#month {
	background-color: rgb(230, 244, 255);
	border: 1px solid rgb(145, 202, 255);
	color: rgb(9, 88, 217);
}

#week {
	background-color: rgb(255, 247, 230);
	border: 1px solid rgb(255, 213, 145);
	color: rgb(212, 107, 8);
}

#day {
	background-color: rgb(249, 240, 255);
	border: 1px solid rgb(211, 173, 247);
	color: rgb(83, 29, 171);
}

.total {
	text-align: center;
}
</style>