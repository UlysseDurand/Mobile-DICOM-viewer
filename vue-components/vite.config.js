export default {
  base: "./",
  build: {
    lib: {
      entry: "./src/main.js",
      name: "mobile_medical_patient_review",
      formats: ["umd"],
      fileName: "mobile_medical_patient_review",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue",
        },
      },
    },
    outDir: "../src/mobile_medical_patient_review/module/serve",
    assetsDir: ".",
  },
};
