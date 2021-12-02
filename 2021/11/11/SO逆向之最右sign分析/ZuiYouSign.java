package com.onejane.zuiyou;

import com.github.unidbg.Module;
import com.github.unidbg.arm.ARMEmulator;
import com.github.unidbg.linux.android.AndroidARMEmulator;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.virtualmodule.android.AndroidModule;

import java.io.File;
import java.io.IOException;


public class ZuiYouSign extends AbstractJni {
    public static void main(String[] args) throws IOException {
        // 1、需要调用的Apk文件所在路径
        String apkFilePath = "F:\\MyProject\\unidbg-onejane\\unidbg-android\\src\\test\\resources\\demo\\zuiyou\\right573.apk";
        // 2、需要调用函数所在的Java类完整路径，比如a/b/c/d等等，注意需要用/代替.
        String classPath = "com/izuiyou/network/NetCrypto";
        // 3、jadx中smali  invoke-static {p0, p1}, Lcom/izuiyou/network/NetCrypto;->sign(Ljava/lang/String;[B)Ljava/lang/String;
        String methodSign = "sign(Ljava/lang/String;[B)Ljava/lang/String;";
        ZuiYouSign runZyObj = new ZuiYouSign(apkFilePath, classPath);
        runZyObj.initCall();
        String InBuf = "50027f7f7f7f8e8e8e8e8e1f1f1f1f1f95896ee5555535a8eecd6aeaab6fd903fd06f629b5081267f2cf11b67199ccf7ced1cf12c36d6c34ed71ac04a95f19c4a7962fd92f0e828e9230ec6439f0906faf716af2f535e1fff5102d85d709610c261cf4d2346a763e842761d66423ec529704972eda6558656e775c499e2dd63f4f402a1437f605f9f2fd17da1b8b90a6235fcaa9c68afd5ae87499df3bfb45ff188836af517cdc91c9d162cc2d8e0efcbfd94b0fabcd6c474ff1cfed1b16f0ea3dcbaa64661c6a0277898c76255d78fc881a59b37dc5733fc9f57e27db914cb80450e1b92ebb0f6defcbddaabc352ca6782b6ad780d838a4389853d5459a1848d847b67287b931752fae05220de2a03212c6cbc165e7b0e96f2e37fb8a83051ad8d35cb4413c90cd89cc743ac9d7c7130526b6acae79867f53b667c51db532a0b9786d69c0e7b9b59910d86a3b9c1964290b7c9a9fe58fd2628f1462c48bbc858327c087eb395733dfb681a9cbc3315c";
        //输出方法调用结果
        String ret = runZyObj.getSign(methodSign
                , new StringObject(runZyObj.vm, "https://zyadapi.izuiyou.com/ad/popup_ad")   //"https://api.izuiyou.com/index/recommend")
                , hexStringToBytes(InBuf));

        // Out Rc=v2-1ff7402d2b4fa9a4c39b3853262f18fd
        System.out.printf("ret:%s\n", ret);
        runZyObj.destroy();
    }

    // ARM模拟器
    private final ARMEmulator emulator;
    // vm
    private final VM vm;
    // 载入的模块
    private final Module module;

    private final DvmClass TTEncryptUtils;


    /**
     *     static {
     *         we5.a(ContextProvider.get(), "net_crypto");
     *         native_init();
     *     }
     * @param apkFilePath  需要执行的apk文件路径
     * @param classPath    需要执行的函数所在的Java类路径
     * @throws IOException
     */
    public ZuiYouSign(String apkFilePath, String classPath) throws IOException {
        // 创建app进程，包名可任意写
        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.onejane.RunZy").build(); // 创建模拟器实例，要模拟32位或者64位，在这里区分
        final Memory memory = emulator.getMemory(); // 模拟器的内存操作接口
        // 作者支持19和23两个sdk
        memory.setLibraryResolver(new AndroidResolver(23));

        // 创建DalvikVM，利用apk本身，可以为null
        vm = ((AndroidARMEmulator) emulator).createDalvikVM(new File(apkFilePath));
        vm.setVerbose(true);
        vm.setJni(this);
        new AndroidModule(emulator, vm).register(memory);

        // （关键处1）加载so，填写so的文件路径
        DalvikModule dm = vm.loadLibrary("net_crypto", false);

        // 调用jni
        dm.callJNI_OnLoad(emulator);
        module = dm.getModule();

        //emulator.traceCode(module.base, module.base + module.size);

        // （关键处2）加载so文件中的哪个类，填写完整的类路径
        TTEncryptUtils = vm.resolveClass(classPath);
    }

    /**
     * 关闭模拟器
     * @throws IOException
     */
    private void destroy() throws IOException {
        emulator.close();
        System.out.println("emulator destroy...");
    }

    /**
     * java.lang.UnsupportedOperationException: com/izuiyou/common/base/BaseApplication->getAppContext()Landroid/content/Context;
     * 	at com.github.unidbg.linux.android.dvm.AbstractJni.callStaticObjectMethodV(AbstractJni.java:426)
     */
    private void initCall() {
        // jeb反编译的smali指令 .method public static native native_init()V
        TTEncryptUtils.callStaticJniMethod(emulator, "native_init()V");
    }

    @Override
    public DvmObject<?> callStaticObjectMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        switch (signature) {
            case "com/izuiyou/common/base/BaseApplication->getAppContext()Landroid/content/Context;":
                return vm.resolveClass("android/content/Context", vm.resolveClass("android/content/ContextWrapper", vm.resolveClass("android/content/Context"))).newObject(signature);
        }

        return super.callStaticObjectMethodV(vm, dvmClass, signature, vaList);
    }

    private String getSign(String methodSign, Object... args) {
        // 使用jni调用传入的函数签名对应的方法（）
        Object value = TTEncryptUtils.callStaticJniMethodObject(emulator, methodSign, args).getValue();
        return value.toString();
    }

    @Override
    public DvmObject<?> callObjectMethodV(BaseVM vm, DvmObject<?> dvmObject, String signature, VaList vaList) {
        switch (signature) {
            case "android/content/Context->getClass()Ljava/lang/Class;":
                return vm.resolveClass("java/lang/Class");
            case "java/lang/Class->getSimpleName()Ljava/lang/String;":
                return new StringObject(vm, "AppController");
            case "android/content/Context->getFilesDir()Ljava/io/File;":
                return vm.resolveClass("java/io/File");
            case "java/lang/Class->getAbsolutePath()Ljava/lang/String;":
                return new StringObject(vm, "/sdcard");
        }
        return super.callObjectMethodV(vm, dvmObject, signature, vaList);
    }

    @Override
    public void callStaticVoidMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        switch (signature) {
            case "cn/xiaochuankeji/tieba/common/debug/AppLogReporter->reportAppRuntime(Ljava/lang/String;Ljava/lang/String;)V":
                return;
        }
        throw new UnsupportedOperationException(signature);
    }

    @Override
    public boolean callStaticBooleanMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        switch (signature) {
            case "android/os/Debug->isDebuggerConnected()Z":
                return Boolean.FALSE;
        }
        return super.callStaticBooleanMethodV(vm,dvmClass,signature,vaList);
    }

    @Override
    public int callStaticIntMethodV(BaseVM vm, DvmClass dvmClass, String signature, VaList vaList) {
        switch (signature) {
            case "android/os/Process->myPid()I":
                return emulator.getPid();
        }
        return super.callStaticIntMethodV(vm,dvmClass,signature,vaList);
    }

    private static byte charToByte(char c) {
        return (byte) "0123456789ABCDEF".indexOf(c);
    }
    public static byte[] hexStringToBytes(String hexString) {
        if (hexString == null || hexString.equals("")) {
            return null;
        }
        hexString = hexString.toUpperCase();
        int length = hexString.length() / 2;
        char[] hexChars = hexString.toCharArray();
        byte[] d = new byte[length];
        for (int i = 0; i < length; i++) {
            int pos = i * 2;
            d[i] = (byte) (charToByte(hexChars[pos]) << 4 | charToByte(hexChars[pos + 1]));

        }
        return d;
    }
}