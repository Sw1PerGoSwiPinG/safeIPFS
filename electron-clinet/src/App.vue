<template>
    <div class="app-container">
        <div class="nav" id="nav">
            <div class="logo">
                <div class="name">SafeIPFS</div><br>
                <div class="author"> Designed by <br> zjy | szt | lxh | lhy </div>
            </div>

            <router-link :to="`/${userId}/home`">
                <div class="nav-item" :class="{ 'active': $route.path === `/${userId}/home` }">系统首页</div>
            </router-link>
            <router-link :to="`/${userId}/create`">
                <div class="nav-item" :class="{ 'active': $route.path === `/${userId}/create` }">创建&上传</div>
            </router-link>
            <router-link :to="`/${userId}/join`">
                <div class="nav-item" :class="{ 'active': $route.path === `/${userId}/join` }">加入&下载</div>
            </router-link>
            <router-link :to="`/${userId}/node`">
                <div class="nav-item" :class="{ 'active': $route.path === `/${userId}/node` }">节点查询</div>
            </router-link>
            <router-link :to="`/${userId}/setting`">
                <div class="nav-item" :class="{ 'active': $route.path === `/${userId}/setting` }">信息配置</div>
            </router-link>
        </div>
        <div style="margin-left: 190px;">
            <router-view />
        </div>
    </div>
</template>

<script>
export default {
    computed: {
        userId() {
            return this.$route.params.userId; // 获取当前用户 ID
        }
    }
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

.container {
    overflow: hidden;
}

.logo {
    padding-left: 30px;
    padding-right: 30px;
}

.name {
    color: #469ea2;
    font-size: xx-large;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
}

.author {
    color: #ffffff;
    margin-bottom: 50px;
}

.nav {
    height: 100%;
    padding-top: 30px;
    padding-bottom: 30px;
    margin-top: -22px;
    position: fixed;
    left: 0;
    top: 0;

    display: flex;
    flex-direction: column;
    background-color: #0b3a53;
}

.nav a {
    font-weight: bold;
    color: #ffffff;
    text-decoration: none;
}

.nav a.router-link-exact-active {
    color: #42b983;
}

.nav-item {
    width: 100%;
    height: auto;
    padding-top: 30px;
    padding-bottom: 30px;
}

.nav-item:hover {
    background-color: #244e65;
    box-shadow: 0 0 10px 5px rgba(0, 0, 0, 0.2);
}

.nav-item.active {
    background-color: #244e65;
    box-shadow: 0 0 10px 5px rgba(0, 0, 0, 0.2);
}
</style>
