<template>
  <div class="login">
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
      <el-form-item label="账号" prop="username">
        <el-input v-model="ruleForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
// import Cookies from 'js-cookie'
export default {
  name: 'Login',
  data () {
    var checkAge = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('账号不能为空'))
      } else {
        callback()
      }
      // setTimeout(() => {
      //   if (!Number.isInteger(value)) {
      //     callback(new Error('请输入数字值'))
      //   } else {
      //     if (value < 18) {
      //       callback(new Error('必须年满18岁'))
      //     } else {
      //       callback()
      //     }
      //   }
      // }, 1000)
    }
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        // if (this.ruleForm.checkPass !== '') {
        //   this.$refs.ruleForm.validateField('checkPass')
        // }
        callback()
      }
    }
    return {
      ruleForm: {
        pass: '',
        username: ''
      },
      rules: {
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        username: [
          {validator: checkAge, trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    submitForm () {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          let formData = new FormData()
          formData.append('UN', this.ruleForm.username)
          formData.append('PW', this.ruleForm.pass)
          this.$djangoAPI.post('/api/login/', formData).then(res => {
            if (res.status) {
              this.$router.push({path: '/home/material'})
            } else {
              this.$message.error('账号或密码错误')
            }
          }).catch(err => {
            console.log(err)
          })
        }
      })
    }
  },
  created: function () {
    // this.$djangoAPI({
    //   url: '/api/login/'
    // }).then(res => {
    //   this.$djangoAPI.interceptors.request.use((config) => {
    //     config.headers['X-Requested-With'] = 'XMLHttpRequest'
    //     config.headers['X-CSRFToken'] = Cookies.get('csrftoken')
    //     return config
    //   })
    // })
  }
}
</script>

<style scoped>
  .demo-ruleForm{
    width: 350px;
    display: inline-block;
    float: left;
    margin-right: 20px;
    position: absolute;
    top: calc(50% - 150px);
    left: calc(50% - 200px);
  }

</style>
