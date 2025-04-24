<template>
  <el-dialog
    title="制作人员"
    :visible.sync="visible"
    :width="isMobile ? '90%' : '50%'"
    :show-close="false"
    :before-close="Close"
  >
    <a
      href="https://www.bilibili.com/video/BV1XmLFz5E7Y/?spm_id_from=333.1387.homepage.video_card.click"
      >视频链接</a
    >
    <div style="display: flex; margin: 10px">
      <div style="width: 120px">
        <el-card :body-style="{ padding: '0px' }">
          <el-image
            style="width: 120px; height: 120px"
            :src="require(`@/assets/img/QAHead.jpg`)"
          ></el-image>
          <div style="padding: 4px">
            <span>QuantAsk</span>
            <br />
            <el-tag size="mini" type="info"> 作者 </el-tag>
          </div>
        </el-card>
      </div>
      <div style="width: 120px; margin-left: 10px">
        <el-card :body-style="{ padding: '0px' }">
          <el-image
            style="width: 120px; height: 120px"
            :src="require(`@/assets/img/GengerHead.jpg`)"
          ></el-image>
          <div style="padding: 4px">
            <span>流明Luminous</span>
            <br />
            <el-tag size="mini" type="info"> ui优化 </el-tag>
          </div>
        </el-card>
      </div>
    </div>

    <span slot="footer" class="dialog-footer">
      <el-button type="primary" @click="Close">确 定</el-button>
    </span>
  </el-dialog>
</template>
<script>
export default {
  name: "About",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isMobile: window.innerWidth <= 768,
    };
  },
  methods: {
    Close() {
      this.$emit("update:visible", false);
    },
  },
};
</script>
