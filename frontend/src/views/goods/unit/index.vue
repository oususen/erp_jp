<template>
  <div>
    <a-card title="製品単位">
      <a-row gutter="16">
        <a-col :span="24" style="max-width: 200px; margin-bottom: 12px;">
          <a-input v-model="searchForm.search" placeholder="名称, 备注" allowClear @pressEnter="search" />
        </a-col>
        <a-col :span="24" style="width: 100px; margin-bottom: 12px;">
          <a-button type="primary" icon="search" @click="search">照会</a-button>
        </a-col>

        <a-col :span="24" style="width: 300px; margin-bottom: 12px;">
          <a-button-group>
            <a-button icon="file-excel" @click="downloadTemplate">テンプレートダウンロード</a-button>
            <a-upload name="file" :showUploadList="false" :customRequest="importExcel">
              <a-button icon="upload">インポート</a-button>
            </a-upload>
            <a-button icon="download" @click="exportExcel">エクスポート</a-button>
          </a-button-group>
        </a-col>

        <div style="margin-bottom: 12px; float: right;">
          <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="openFormModal(form)">新增单位</a-button>
        </div>
      </a-row>

      <a-row style="margin-top: 12px;">
        <a-table size="small" :columns="columns" :dataSource="items" rowKey="id" :loading="loading" :pagination="pagination"
          @change="tableChange">
          <div slot="is_active" slot-scope="value">
            <a-tag :color="value ? 'green' : 'red'">{{value ? '有効' : '無効'}}</a-tag>
          </div>
          <div slot="action" slot-scope="value, item">
            <a-button-group>
              <a-button icon="edit" size="small" @click="openFormModal(item)">編集</a-button>
              <a-popconfirm title="削除してもよろしいですか" @confirm="destroy(item.id)">
                <a-button type="danger" icon="delete" size="small">削除</a-button>
              </a-popconfirm>
            </a-button-group>
          </div>
        </a-table>
      </a-row>
    </a-card>
    <form-modal v-model="visible" :form="targetItem" @create="create" @update="update" />
    <a-modal v-model="importLoading" :footer="null" :maskClosable="false" :closable="false">
      <div>
        <a-spin style="margin-right: 12px;" />正在导入中, 请等待...
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { exportExcel } from '@/utils/excel'
  import { goodsUnitExport } from '@/api/export'
  import { goodsUnitTemplate, goodsUnitImport } from '@/api/import'
  import { goodsUnitList, goodsUnitDestroy } from '@/api/goods'

  export default {
    name: 'Warehouse',
    components: {
      FormModal: () => import('./FormModal.vue'),
    },
    data() {
      return {
        columns: [
          {
            title: '番号',
            dataIndex: 'index',
            key: 'index',
            customRender: (value, item, index) => {
              return index + 1
            },
          },
          {
            title: '单位名称',
            dataIndex: 'name',
            sorter: true,
          },
          {
            title: '備考',
            dataIndex: 'remark'
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: '156px'
          },
        ],
        searchForm: { search: '', page: 1, page_size: 16 },
        pagination: { current: 1, total: 0, pageSize: 16 },
        loading: false,
        items: [],

        visible: false,
        targetItem: {},
        form: {},
        importLoading: false,
      };
    },
    computed: {
    },
    methods: {
      initialize() {
        this.list();
      },
      list() {
        this.loading = true;
        goodsUnitList(this.searchForm).then(data => {
          this.pagination.total = data.count;
          this.items = data.results;
        }).finally(() => {
          this.loading = false;
        });
      },
      create(item) {
        // this.items.splice(0, 0, item);
        this.list();
      },
      update(item) {
        this.items.splice(this.items.findIndex(i => i.id == item.id), 1, item);
      },
      search() {
        this.searchForm.page = 1;
        this.pagination.current = 1;
        this.list();
      },
      openFormModal(item) {
        this.targetItem = { ...item };
        this.visible = true;
      },
      destroy(id) {
        goodsUnitDestroy({ id }).then(() => {
          // this.items.splice(this.items.findIndex(item => item.id == id), 1);
          this.$message.success('删除成功');
          this.list();
        });
      },
      exportExcel() {
        goodsUnitExport(this.searchForm).then(resp => {
          exportExcel(resp.data, '产品单位列表');
        }).catch(err => {
          this.$message.error(err.response.data.error);
        });
      },
      downloadTemplate () {
        goodsUnitTemplate().then(resp => {
          exportExcel(resp.data, '产品单位导入模板');
        }).catch(err => {
          this.$message.error(err.response.data.error);
        });
      },
      importExcel(item) {
        let data = new FormData();
        data.append('file', item.file);
        this.importLoading = true;
        setTimeout(() => {
          goodsUnitImport(data)
            .then(() => {
              this.$message.success('导入成功');
              this.list();
            })
            .catch(err => {
              this.$message.error(err.response.data.detail);
            })
            .finally(() => {
              this.importLoading = false;
            });
        }, 1000);
      },
      tableChange(pagination, filters, sorter) {
        this.searchForm.page = pagination.current;
        this.pagination.current = pagination.current;
        this.searchForm.ordering = `${sorter.order == 'descend' ? '-' : ''}${sorter.field}`;
        this.list();
      },
    },
    mounted() {
      this.initialize();
    },
  }
</script>