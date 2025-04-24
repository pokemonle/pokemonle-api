<template>
  <el-dialog
    title="规则介绍"
    :visible.sync="visible"
    :width="isMobile ? '90%' : '50%'"
    :show-close="false"
    :before-close="Close"
    custom-class="enhanced-dialog"
  >
    <div class="intro-content">
      <p>输入一个宝可梦进行猜测。</p>
      <p>每次猜测后，你会获得你输入的宝可梦的信息。</p>
      <div class="hint-section">
        <div class="hint-item">
          <el-tag type="success" size="small">绿色高亮</el-tag>
          <span>表示该信息与你需要猜测的宝可梦完全相同</span>
        </div>
        <div class="hint-item">
          <el-tag type="warning" size="small">黄色高亮</el-tag>
          <span>表示该信息与你需要猜测的宝可梦比较接近</span>
        </div>
        <div class="hint-item">
          <span>"↑": 应该往高了猜；"↓": 应该往低了猜</span>
        </div>
      </div>
      <p>简单模式只会保留较为热门或携带其他标签的宝可梦。</p>
      <p><strong>世代选择：</strong>可以选择单个或多个世代组合进行游戏。</p>
      <p>
        <strong>随机开局：</strong
        >帮你随机选择一个当前世代范围内的宝可梦作为第一次猜测。
      </p>
    </div>

    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="Close">确 定</el-button>
    </div>
  </el-dialog>
</template>
<script>
export default {
  name: "Intro",
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
