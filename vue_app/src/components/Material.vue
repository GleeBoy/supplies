<template>
  <div>
    <el-form :inline="true" :model="formInline" class="demo-form-inline">
      <el-form-item label="搜索">
        <el-input v-model="formInline.search"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" round @click="onSearch">查询</el-button>
      </el-form-item>
<!--      v-if="permissions" -->
      <el-button type="primary" round @click="openDialog">添加</el-button>
    </el-form>
    <el-dialog title="" :visible.sync="dialogFormVisible">
      <el-form :model="materForm" :rules="rules" ref="materForm" status-icon  class="addForm">
        <el-form-item label="中安料号" prop="item_code">
          <div v-if="!materForm.id">
            <el-select v-model="materForm.superClass" style="width: 150px" placeholder="请选择父类" @change="searchSub">
              <el-option
                v-for="item in superClass"
                :key="item.code"
                :label="item.name"
                :value="item.code">
              </el-option>
            </el-select>
            <el-select style="width: 150px" v-model="materForm.item_name" placeholder="请选择子类" @change="getMiddleStr">  <!-- @change="getMiddleStr" -->
              <el-option
                v-for="item in subClass"
                :key="item.id"
                :label="item.name"
                :value="item">
              </el-option>
            </el-select>
            <el-input v-model="materForm.middleStr" @change="getItemCode" placeholder="5位编号" maxlength="5" minlength="5" autocomplete="off"></el-input>
            <el-input v-model="materForm.lastStr" @change="getItemCode" maxlength="2" minlength="2" autocomplete="off"></el-input>
          </div>

          <el-input v-model="materForm.item_code" style="width: 500px" readonly autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类别" prop="item_name">
          <el-input v-model="materForm.item_name" style="width: 150px" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="materForm.describe" style="width: 500px" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="厂商型号" prop="firm_code">
          <el-input v-model="materForm.firm_code" style="width: 150px" autocomplete="off"></el-input>
          <label>厂商</label> <el-input v-model="materForm.firm_name" style="width: 150px" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="物料照片">
          <el-upload
            action="#"
            list-type="picture-card"
            :limit="1"
            :file-list="imgList"
            :auto-upload="false"
            :on-change="handleChange">
            <i slot="default" class="el-icon-plus"></i>
            <div slot="file" slot-scope="{file}">
              <img
                class="el-upload-list__item-thumbnail"
                :src="file.url" alt=""
              >
              <span class="el-upload-list__item-actions">
                <span
                  v-if="!disabled"
                  class="el-upload-list__item-delete"
                  @click="handleRemove(file)"
                >
                  <i class="el-icon-delete"></i>
                </span>
              </span>
            </div>
          </el-upload>

          <el-upload
            action="#"
            list-type="picture-card"
            :http-request="uploadImg"
            :file-list="materForm.media_img">
<!--                        :auto-upload="false"-->
            <i slot="default" class="el-icon-plus"></i>
            <div slot="file" slot-scope="{file}">
              <img
                class="el-upload-list__item-thumbnail"
                :src="file.file_path" alt="">
              <span class="el-upload-list__item-actions">
<!--                <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">-->
<!--                  <i class="el-icon-zoom-in"></i>-->
<!--                </span>-->
<!--                <span-->
<!--                  v-if="!disabled"-->
<!--                  class="el-upload-list__item-delete"-->
<!--                  @click="handleDownload(file)"-->
<!--                >-->
<!--                  <i class="el-icon-download"></i>-->
<!--                </span>-->
                <span
                  v-if="!disabled"
                  class="el-upload-list__item-delete"
                  @click="removeImg(file)"
                >
                  <i class="el-icon-delete"></i>
                </span>
              </span>
            </div>
          </el-upload>

        </el-form-item>
        <el-form-item label="规格书">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            :limit="1"
            :on-change="specification"
            :on-remove="rmSpec"
            :file-list="fileList"
            :auto-upload="false">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
<!--            <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>-->
          </el-upload>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="materForm.remark" style="width: 500px" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addM">确 定</el-button>
      </div>
    </el-dialog>
    <el-table
      :data="tableData"
      style="width: 100%"
      @row-click="marInfo"
    >
<!--      :default-sort="{prop: 'item_code', order: 'descending'}"-->
      <el-table-column
        prop="item_code"
        label="中安料号"
        sortable
        width="180">
      </el-table-column>
      <el-table-column
        prop="item_name"
        label="类别"
        sortable
        width="180">
      </el-table-column>
      <el-table-column
        prop="describe"
        label="描述">
      </el-table-column>
      <el-table-column
        prop="firm_code"
        label="厂商型号"
        sortable
        width="180">
      </el-table-column>
      <el-table-column
        prop="firm_name"
        label="厂商名字"
        sortable>
      </el-table-column>
      <el-table-column
        label="物料照片">
        <template slot-scope="scope">
          <el-image v-if="scope.row.material_img"
            style="width: 50px; height: 50px"
            :src="scope.row.material_img"
            ></el-image>
          <label v-else></label>
        </template>
      </el-table-column>
      <el-table-column
        label="规格书">
        <template slot-scope="scope">
<!--          <a :href="scope.row.specification">{{ scope.row.specification | fileName }}</a>-->
          {{ scope.row.specification | fileName }}
        </template>
      </el-table-column>
      <el-table-column
        prop="remark"
        label="备注"
        width="180">
      </el-table-column>
      <el-table-column
        prop="record_time"
        label="创建时间">
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="pagination.current"
      :page-sizes="pagination.limitList"
      :page-size="pagination.limit"
      layout="total, sizes, prev, pager, next, jumper"
      :total="pagination.count">
    </el-pagination>
    <el-dialog title="物料信息" :visible.sync="marVisible">
      <el-form :model="materForm" status-icon  class="addForm">
        <el-form-item label="中安料号">
          <el-input v-model="materForm.item_code" style="width: 500px" readonly autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="类别">
          <el-input v-model="materForm.item_name" readonly autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="materForm.describe" readonly style="width: 500px" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="厂商型号">
          <el-input v-model="materForm.firm_code" readonly autocomplete="off"></el-input>
          <label>厂商</label> <el-input v-model="materForm.firm_name" readonly autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="物料照片">
          <div v-if="materForm.material_img instanceof Object"></div>
          <el-image v-else style="width: 50px; height: 50px"
                    :src="materForm.material_img"
                    :preview-src-list="[materForm.material_img]"
                    :z-index="2100"></el-image>
          <el-image style="width: 50px; height: 50px; margin-left: 5px"
                    v-for="img in materForm.media_img"
                    :key="img.id"
                    :src="img.file_path"
                    :preview-src-list="[img.file_path]"
                    :z-index="2100"></el-image>
        </el-form-item>
        <el-form-item label="规格书">
          <a :href="materForm.specification">{{ materForm.specification | fileName }}</a>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="materForm.remark" readonly style="width: 500px" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="操作员">
          <el-input v-model="materForm.user" readonly style="width: 500px" autocomplete="off"></el-input>
        </el-form-item>
<!--         v-if="permissions"-->
        <el-form-item label="操作">
          <el-button type="primary" icon="el-icon-edit" circle @click="editMaterial"></el-button>
          <el-button type="danger" icon="el-icon-delete" circle @click="deleteMaterial"></el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import Cookies from 'js-cookie'

export default {
  name: 'Material',
  data () {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('不可为空'))
      } else {
        callback()
      }
    }
    // var checkFirm = (rule, value, callback) => {
    //   if (this.materForm.firm_code === '' || this.materForm.firm_name === '') {
    //     callback(new Error('不可为空'))
    //   } else {
    //     if (this.materForm.id) {
    //       callback()
    //     } else {
    //       if (this.materForm.firm_name === '中安百傲') {
    //         callback()
    //       } else {
    //         let params = {
    //           params: {
    //             firm_code: this.materForm.firm_code,
    //             firm_name: this.materForm.firm_name
    //           }
    //         }
    //         this.$djangoAPI.get('/api/check_firm/', params).then(res => {
    //           if (res.results === 'yes') {
    //             callback(new Error('厂商型号，厂商已存在'))
    //           } else {
    //             callback()
    //           }
    //         })
    //       }
    //     }
    //   }
    // }
    var checkItemcode = (rule, value, callback) => {
      if (this.materForm.item_code === '') {
        callback(new Error('不可为空'))
      } else {
        if (this.materForm.id) {
          callback()
        } else {
          if (this.materForm.middleStr.length !== 5 || this.materForm.lastStr.length !== 2) {
            callback(new Error('物料编号位数不对'))
          } else {
            let params = {
              params: {
                item_code: this.materForm.item_code
              }
            }
            this.$djangoAPI.get('/api/check_itemcode/', params).then(res => {
              if (res.results === 'yes') {
                callback(new Error('物料已存在'))
              } else {
                callback()
              }
            })
          }
        }
      }
    }
    return {
      imgUrl: '/static/123.jpg',
      formInline: {
        search: ''
      },
      tableData: [],
      pagination: {
        current: 1,
        limit: 20,
        count: 0,
        limitList: [20, 50, 100, 300]
      },
      dialogFormVisible: false,
      superClass: [],
      subClass: [],
      materForm: {
        id: '',
        superClass: '',
        subClass: '',
        middleStr: '',
        lastStr: '',
        item_code: '',
        item_name: '',
        describe: '',
        firm_code: '',
        firm_name: '',
        remark: '',
        material_img: null,
        specification: null,
        media_img: []
      },
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      rules: {
        item_code: [
          {validator: checkItemcode, trigger: 'blur'}
        ],
        item_name: [
          {validator: validatePass, trigger: 'blur'}
        ]
        // firm_code: [
        //   {validator: checkFirm, trigger: 'blur'}
        // ]
      },
      imgList: [],
      fileList: [],
      marVisible: false
      // permissions: false
    }
  },
  methods: {
    onSearch () {
      let params = {
        params: {
          search: this.formInline.search,
          page: this.pagination.current,
          page_size: this.pagination.limit
        }
      }
      this.$djangoAPI.get('/api/manage/materialinfo/', params).then(res => {
        this.pagination.count = res.count
        this.tableData = res.results
      })
    },
    handleSizeChange (val) {
      this.pagination.limit = val
      this.onSearch()
    },
    handleCurrentChange (val) {
      this.pagination.current = val
      this.onSearch()
    },
    searchSub () {
      this.$djangoAPI.get('/api/manage/subclass/', {params: {search: this.materForm.superClass}}).then(res => {
        this.subClass = res.results
        this.materForm.subClass = this.subClass[0].code
        this.materForm.item_name = this.subClass[0].name
        this.getMiddleStr(this.subClass[0])
      })
    },
    getMiddleStr (val) {
      this.materForm.item_name = val.name
      this.materForm.subClass = val.code
      // let params = {params: {superClass: this.materForm.superClass, subClass: this.materForm.subClass}}
      // this.$djangoAPI.get('/api/middle_str/', params).then(res => {
      //   this.materForm.middleStr = res.results
      this.getItemCode()
      // })
    },
    getItemCode () {
      if (this.materForm.lastStr) { // 确保lastStr不为空
        this.materForm.item_code = this.materForm.superClass + this.materForm.subClass + '-' + this.materForm.middleStr + '-' + this.materForm.lastStr
      }
    },
    openDialog (row) {
      this.initMaterForm()
      this.$djangoAPI.get('/api/manage/superclass/').then(res => {
        this.superClass = res.results
        this.materForm.superClass = this.superClass[0].code
        this.searchSub()
      })
      // this.$djangoAPI.get('/api/manage/subclass/', {params: {search: this.materForm.superClass}}).then(res => {
      //   this.subClass = res.results
      // })
      this.dialogFormVisible = true
    },
    handleRemove (file) {
      this.imgList = []
      this.materForm.material_img = null
    },
    addM () {
      this.$refs['materForm'].validate((valid) => {
        if (valid) {
          let formData = new FormData()
          formData.append('item_code', this.materForm.item_code)
          formData.append('item_name', this.materForm.item_name)
          if (this.materForm.describe) {
            formData.append('describe', this.materForm.describe)
          } else {
            formData.append('describe', '')
          }
          formData.append('firm_code', this.materForm.firm_code)
          formData.append('firm_name', this.materForm.firm_name)
          if (this.materForm.material_img instanceof Object) {
            formData.append('material_img', this.materForm.material_img.raw)
          } else if (!this.materForm.material_img) {
            formData.append('material_img', '')
          }
          if (this.materForm.specification instanceof Object) {
            formData.append('specification', this.materForm.specification.raw)
          } else if (!this.materForm.specification) {
            formData.append('specification', '')
          }
          if (this.materForm.remark) {
            formData.append('remark', this.materForm.remark)
          } else {
            formData.append('remark', '')
          }
          // formData.append('user', Cookies.get('username'))
          if (this.materForm.id) {
            let url = '/api/manage/materialinfo/' + this.materForm.id + '/'
            this.$djangoAPI.put(url, formData, {headers: {'Content-Type': 'multipart/form-data'}}).then(res => {
              this.dialogFormVisible = false
              this.$message({
                type: 'success',
                message: '修改成功!'
              })
              this.onSearch()
            })
          } else {
            var idStr = ''
            for (var i in this.materForm.media_img) {
              idStr += this.materForm.media_img[i]['id'] + ','
            }
            formData.append('media_img', idStr)
            this.$djangoAPI.post('/api/manage/materialinfo/', formData, {headers: {'Content-Type': 'multipart/form-data'}}).then(res => {
              this.dialogFormVisible = false
              this.$message({
                type: 'success',
                message: '添加成功!'
              })
              this.onSearch()
            })
          }
        }
      })
    },
    handleChange (file, imgList) {
      this.materForm.material_img = file
    },
    specification (file, imgList) {
      this.materForm.specification = file
    },
    rmSpec (file, fileList) {
      this.materForm.specification = null
    },
    initMaterForm () {
      this.materForm = {
        superClass: '',
        subClass: '',
        middleStr: '',
        lastStr: '01',
        item_code: '',
        item_name: '',
        describe: '',
        firm_code: '',
        firm_name: '',
        remark: '',
        material_img: null,
        specification: null,
        media_img: []
      }
      this.imgList = []
      this.fileList = []
    },
    editMaterial () {
      this.marVisible = false
      this.dialogFormVisible = true
      // if (this.superClass.id) {
      //       let url = '/api/manage/superclass/' + this.superClass.id + '/'
      //       this.$djangoAPI.put(url, formData).then(res => {
      //         this.$message.success('修改成功')
      //       })
      //     }
    },
    deleteMaterial () {
      this.$confirm('此操作将永久删除这条物料信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.marVisible = false
        let url = '/api/manage/materialinfo/' + this.materForm.id + '/'
        this.$djangoAPI.delete(url).then(res => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.onSearch()
        })
      })
    },
    marInfo (row) {
      this.marVisible = true
      this.materForm.id = row.id
      this.materForm.item_code = row.item_code
      this.materForm.item_name = row.item_name
      this.materForm.describe = row.describe
      this.materForm.firm_code = row.firm_code
      this.materForm.firm_name = row.firm_name
      this.materForm.remark = row.remark
      this.materForm.material_img = row.material_img
      this.materForm.specification = row.specification
      this.materForm.user = row.user
      this.materForm.media_img = row.media_img
      if (row.material_img) {
        this.imgList = [{url: row.material_img}]
      } else {
        this.imgList = []
      }
      if (row.specification) {
        this.fileList = [{url: row.specification, name: this.$options.filters['fileName'](row.specification)}]
      } else {
        this.fileList = []
      }
    },
    // handlePictureCardPreview (file) {
    //   this.dialogImageUrl = file.url
    //   this.dialogVisible = true
    // },
    handleDownload (file) {
      console.log(file)
    },
    uploadImg: function (f) {
      let formData = new FormData()
      formData.append('file_path', f.file)
      formData.append('file_name', f.file.name)
      if (this.materForm.id) {
        formData.append('materialinfo', this.materForm.id)
      }
      this.$djangoAPI.post('/api/manage/mediaimg/', formData, {headers: {'Content-Type': 'multipart/form-data'}}).then(res => {
        this.materForm.media_img.push(res)
      })
    },
    removeImg (file) {
      this.$confirm('此操作将永久删除这张图片, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let url = '/api/manage/mediaimg/' + file.id + '/'
        this.$djangoAPI.delete(url).then(res => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          let index = this.getIndex(this.materForm.media_img, file)
          this.materForm.media_img.splice(index, 1)
        })
      })
    }
  },
  created: function () {
    this.onSearch()
  },
  beforeCreate: function () {
    this.permissions = Cookies.get('permissions')
  }
}
</script>

<style scoped>
  .addForm .el-input{
    width: 100px;
  }

</style>
