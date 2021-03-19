<template>
  <div class="hello">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex2"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b">
          <el-menu-item index="material">物料管理</el-menu-item>
          <el-menu-item index="kind">种类管理</el-menu-item>
          <el-tooltip class="item" effect="dark" :content="user.username" placement="left">
            <el-button @click="logout" class="logout" type="primary" icon="el-icon-user-solid" round size="small">退出登录</el-button>
          </el-tooltip>
        </el-menu>
      </el-header>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
export default {
  name: 'HelloWorld',
  components: {
  },
  data () {
    return {
      activeIndex2: 'material',
      user: {
        id: '',
        username: ''
      }
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      // this.$router.push({path: '/' + key})
      this.$router.push({path: key})
    },
    logout () {
      this.$djangoAPI.get('/api/logout/').then(
        res => {
          this.$router.push({path: '/', name: 'Login'})
        }
      )
    }
  },
  created: function () {
    this.user.id = Cookies.get('id')
    this.user.username = Cookies.get('username')
    // this.$router.push({path: 'material'})
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.logout{
  float: right;
  margin: 13px;
}
</style>
