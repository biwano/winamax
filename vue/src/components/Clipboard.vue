<template>
  <span
    >&nbsp;<i class="fas fa-copy clickable" @click="copyTextToClipboard()"></i
  ></span>
</template>

<script>
export default {
  name: "MatchesMarks",
  props: ["text"],
  methods: {
    fallbackCopyTextToClipboard(text) {
      var textArea = document.createElement("textarea");
      textArea.value = text;

      // Avoid scrolling to bottom
      textArea.style.top = "0";
      textArea.style.left = "0";
      textArea.style.position = "fixed";

      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      try {
        var successful = document.execCommand("copy");
        var msg = successful ? "successful" : "unsuccessful";
        console.log("Fallback: Copying text command was " + msg);
      } catch (err) {
        console.error("Fallback: Oops, unable to copy", err);
      }

      document.body.removeChild(textArea);
    },
    copyTextToClipboard() {
      if (!navigator.clipboard) {
        this.fallbackCopyTextToClipboard(this.text);
        return;
      }
      navigator.clipboard.writeText(this.text).then(
        function() {
          console.log("Async: Copying to clipboard was successful!");
        },
        function(err) {
          console.error("Async: Could not copy text: ", err);
        }
      );
    },
  },
};
</script>
