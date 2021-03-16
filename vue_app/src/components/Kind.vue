<template>
  <div>
    <div>
      <el-button type="primary" round size="medium" @click="addSuper">添加父类</el-button>
      <el-button type="primary" round size="medium" @click="addSub">添加子类</el-button>
    </div>
    <el-divider>父类</el-divider>
    <el-table
      :data="tableData1"
      height="300"
      border
      style="width: 100%">
      <el-table-column
        prop="code"
        label="编号"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="名字"
        width="180">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述">
      </el-table-column>
      <el-table-column
        label="操作">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle @click="editSuper(scope.row)"></el-button>
          <el-button type="danger" icon="el-icon-delete" circle @click="deleteSuper(scope.row.id)"></el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-divider>子类</el-divider>
    <el-table
      :data="tableData2"
      height="600"
      style="width: 100%">
      <el-table-column
        prop="superclass"
        label="父类"
        width="180">
      </el-table-column>
      <el-table-column
        prop="code"
        label="编号"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="名字"
        width="180">
      </el-table-column>
      <el-table-column
        prop="example"
        label="例子">
      </el-table-column>
      <el-table-column
        label="操作">
        <template slot-scope="scope">
        <el-button type="primary" icon="el-icon-edit" circle @click="editSub(scope.row)"></el-button>
        <el-button type="danger" icon="el-icon-delete" circle @click="deleteSub(scope.row.id)"></el-button>
      </template>
      </el-table-column>
    </el-table>
    <el-dialog title="" :visible.sync="dialogFormVisible">
      <el-form ref="superForm" :model="superClass" label-width="80px" :rules="rules">
        <el-form-item label="编码" prop="code">
          <el-input v-model="superClass.code" placeholder="必须是两位"></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="superClass.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="superClass.description"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addEditSuperClass">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="" :visible.sync="subVisible">
      <el-form ref="subForm" :model="subClass" label-width="80px" :rules="subRules">
        <el-form-item label="父类" prop="superclass">
          <el-select v-model="subClass.superclass" :disabled="editSubSuper" placeholder="请选择父类" @change="subCode">
            <el-option
              v-for="item in tableData1"
              :key="item.id"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="编码">
          <el-input v-model="subClass.code" readonly></el-input>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="subClass.name"></el-input>
        </el-form-item>
        <el-form-item label="例子">
          <el-input v-model="subClass.example"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="subVisible = false">取 消</el-button>
        <el-button type="primary" @click="addEditSub">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Kind',
  data () {
    var supCodeHttp = (callback) => {
      this.$djangoAPI.get('/check_super_code/', {params: {code: this.superClass.code}}).then(res => {
        if (res.results === 'yes') {
          callback(new Error('编码已存在'))
        } else {
          callback()
        }
      })
    }
    var checkSuperCode = (rule, value, callback) => {
      if (this.superClass.id) {
        if (this.superClass.copyCode === this.superClass.code) {
          callback()
        } else {
          supCodeHttp(callback)
        }
      } else {
        supCodeHttp(callback)
      }
    }
    var supNameHttp = (callback) => {
      this.$djangoAPI.get('/check_super_name/', {params: {name: this.superClass.name}}).then(res => {
        if (res.results === 'yes') {
          callback(new Error('名称已存在'))
        } else {
          callback()
        }
      })
    }
    var checkSuperName = (rule, value, callback) => {
      if (this.superClass.id) {
        if (this.superClass.copyName === this.superClass.name) {
          callback()
        } else {
          supNameHttp(callback)
        }
      } else {
        supNameHttp(callback)
      }
    }
    var subNameHttp = (callback) => {
      this.$djangoAPI.get('/check_sub_name/', {params: {super_name: this.subClass.superclass, name: this.subClass.name}}).then(res => {
        if (res.results === 'yes') {
          callback(new Error('这个父类下的子类名称已存在'))
        } else {
          callback()
        }
      })
    }
    var checkSubName = (rule, value, callback) => {
      if (this.subClass.id) {
        if (this.subClass.copyName === this.subClass.name) {
          callback()
        } else {
          subNameHttp(callback)
        }
      } else {
        subNameHttp(callback)
      }
    }
    return {
      tableData1: [],
      tableData2: [],
      dialogFormVisible: false,
      subVisible: false,
      superClass: {
        id: '',
        code: '',
        name: '',
        description: '',
        // 编辑时验证是否改变
        copyCode: '',
        copyName: ''
      },
      subClass: {
        id: '',
        superclass: '',
        code: '',
        name: '',
        example: '',
        copyName: ''
      },
      rules: {
        code: [
          {required: true, message: '请输入编码', trigger: 'blur'},
          {min: 2, max: 2, message: '长度是2个字符', trigger: 'blur'},
          {validator: checkSuperCode, trigger: 'blur'}
        ],
        name: [
          {required: true, message: '请输入名称', trigger: 'blur'},
          {min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur'},
          {validator: checkSuperName, trigger: 'blur'}
        ]
      },
      subRules: {
        superclass: [
          {required: true, message: '请选择父类', trigger: 'blur'}
        ],
        name: [
          {required: true, message: '请输入名称', trigger: 'blur'},
          {min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur'},
          {validator: checkSubName, trigger: 'blur'}
        ]
      },
      editSubSuper: false
    }
  },
  methods: {
    getSuperClass () {
      this.$djangoAPI.get('/manage/superclass/').then(res => {
        this.tableData1 = res.results
      })
    },
    getSubClass () {
      // subclass
      this.$djangoAPI.get('/manage/subclass/').then(res => {
        this.tableData2 = res.results
      })
    },
    addEditSuperClass () {
      this.$refs['superForm'].validate((valid) => {
        if (valid) {
          let formData = new FormData()
          formData.append('code', this.superClass.code)
          formData.append('name', this.superClass.name)
          if (this.superClass.description) {
            formData.append('description', this.superClass.description)
          }
          if (this.superClass.id) {
            let url = '/manage/superclass/' + this.superClass.id + '/'
            this.$djangoAPI.put(url, formData).then(res => {
              this.$message.success('修改成功')
              this.dialogFormVisible = false
              this.getSuperClass()
              this.getSubClass()
            })
          } else {
            this.$djangoAPI.post('/manage/superclass/', formData).then(res => {
              this.$message.success('添加成功')
              this.dialogFormVisible = false
              this.getSuperClass()
            })
          }
        }
      })
    },
    editSuper (row) {
      this.dialogFormVisible = true
      this.superClass.code = row.code
      this.superClass.name = row.name
      this.superClass.description = row.description
      this.superClass.id = row.id
      this.superClass.copyCode = row.code
      this.superClass.copyName = row.name
    },
    initSuper () {
      this.superClass = {
        id: '',
        code: '',
        name: '',
        description: ''
      }
    },
    addSuper () {
      this.dialogFormVisible = true
      this.initSuper()
    },
    deleteSuper (id) {
      this.$confirm('此操作将永久删除父类和这个父类下的子类, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let url = '/manage/superclass/' + id + '/'
        this.$djangoAPI.delete(url).then(res => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getSuperClass()
          this.getSubClass()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    initSub () {
      this.subClass = {
        id: '',
        superclass: '',
        code: '',
        name: '',
        example: ''
      }
    },
    addSub () {
      this.subVisible = true
      this.initSub()
      this.editSubSuper = false
    },
    addEditSub () {
      this.$refs['subForm'].validate((valid) => {
        if (valid) {
          let formData = new FormData()
          formData.append('superclass', this.subClass.superclass)
          formData.append('code', this.subClass.code)
          formData.append('name', this.subClass.name)
          if (this.subClass.example) {
            formData.append('example', this.subClass.example)
          }
          if (this.subClass.id) {
            let url = '/manage/subclass/' + this.subClass.id + '/'
            this.$djangoAPI.put(url, formData).then(res => {
              this.$message.success('修改成功')
              this.subVisible = false
              this.getSubClass()
            })
          } else {
            this.$djangoAPI.post('/manage/subclass/', formData).then(res => {
              this.$message.success('添加成功')
              this.subVisible = false
              this.getSubClass()
            })
          }
        }
      })
    },
    subCode () {
      this.$djangoAPI.get('/get_sub/', {params: {superName: this.subClass.superclass}}).then(res => {
        this.subClass.code = res.sub_code
      })
    },
    editSub (row) {
      this.subVisible = true
      this.editSubSuper = true
      this.subClass.superclass = row.superclass
      this.subClass.code = row.code
      this.subClass.name = row.name
      this.subClass.example = row.example
      this.subClass.id = row.id
      this.subClass.copyName = row.name
    },
    deleteSub (id) {
      this.$confirm('此操作将永久删除子类, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let url = '/manage/subclass/' + id + '/'
        this.$djangoAPI.delete(url).then(res => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getSubClass()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
  },
  created: function () {
    this.getSuperClass()
    this.getSubClass()
  }
}
</script>

<style scoped>

</style>
