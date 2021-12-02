package com.example.onejanexposed;

import android.util.Log;

import org.apache.commons.lang3.StringUtils;

import java.io.IOException;
import java.util.Map;

import de.robv.android.xposed.IXposedHookLoadPackage;
import de.robv.android.xposed.XposedBridge;
import de.robv.android.xposed.XposedHelpers;
import de.robv.android.xposed.callbacks.XC_LoadPackage;
import fi.iki.elonen.NanoHTTPD;


public class HookLoader implements IXposedHookLoadPackage {
    private final static String TAG = "onejane";
    public static void log(String s) {
        Log.i(TAG, s);
    }

    public void handleLoadPackage(final XC_LoadPackage.LoadPackageParam loadPackageParam) throws Throwable {

         log("Im comming "+loadPackageParam.packageName);
         XposedBridge.log("xposed log Hooked Frist!");

        if (loadPackageParam.packageName.equals("cn.xiaochuankeji.tieba")) {
            log("Im comming zy 3");


            // http server
            class myHttpServer extends NanoHTTPD {
                private static  final String REQUEST_ROOT = "/";

                public myHttpServer() throws IOException {
                    // 端口是8088，也就是说要通过http://127.0.0.1:8088来访当问
                    super(8888);
                    start(NanoHTTPD.SOCKET_READ_TIMEOUT, true);
                    log("---fenfei Server---");
                }

                @Override
                public Response serve(IHTTPSession session) {
                    // log("serve");
                    //这个就是之前分析，重写父类的一个参数的方法，
                    //这里边已经把所有的解析操作已经在这里执行了
                    return super.serve(session);
                }

                @Override
                public Response serve(String uri, Method method, Map<String, String> headers, Map<String, String> parms, Map<String, String> files) {
                    // log("serve xxx");
                    //这就是上边的serve方法最后一行调用的那个过时的方法，这里简单的做个判断就好了
                    // if (!method.equals(Method.POST)) {//判断请求方式是否争取
                    //    return newFixedLengthResponse("the request method is incoorect");
                    // }

                    log(uri);

                     for (Map.Entry<String, String> entry : files.entrySet()) {
                         log("Key = " + entry.getKey() + ", Value = " + entry.getValue());
                     }


                    Class<?> clazzZy = null;
                    try {
                        clazzZy = loadPackageParam.classLoader.loadClass("com.izuiyou.network.NetCrypto");
                        log("load class:" + clazzZy);
                    } catch (Exception e) {
                        log("load class err:" + Log.getStackTraceString(e));
                        return newFixedLengthResponse("load class is null");
                    }

                    if (StringUtils.containsIgnoreCase(uri, "getkey")) {//判断uri是否正确
                        return getKey(clazzZy);
                    }

                    if (StringUtils.containsIgnoreCase(uri, "setkey")) {//判断uri是否正确
                        String postData = files.get("postData");
                        if (!StringUtils.isEmpty(postData)) {//判断post过来的数据是否正确
                            return setkey(clazzZy,postData);
                        }else{
                            return newFixedLengthResponse("postData is null");
                        }
                    }

                    if (StringUtils.containsIgnoreCase(uri, "sign")) {
                        String postData = files.get("postData");
                        if (!StringUtils.isEmpty(postData)) {
                            return sign(clazzZy,postData);
                        }else{
                            return newFixedLengthResponse("postData is null");
                        }
                    }

                    if (StringUtils.containsIgnoreCase(uri, "aesenc")) {
                        String postData = files.get("postData");
                        if (!StringUtils.isEmpty(postData)) {
                            return aesenc(clazzZy,postData);
                        }else{
                            return newFixedLengthResponse("postData is null");
                        }
                    }


                    if (StringUtils.containsIgnoreCase(uri, "aesdec")) {//判断uri是否正确
                        String postData = files.get("postData");
                        if (!StringUtils.isEmpty(postData)) {//判断post过来的数据是否正确
                            return aesdec(clazzZy,postData);
                        }else{
                            return newFixedLengthResponse("postData is null");
                        }
                    }


                    //判断完了开始解析数据，如果是你想要的数据，那么你就给返回一个正确的格式就好了
                    //举个栗子：return newFixedLengthResponse("{\"result\":0,\"success\":true}");
                    return super.serve(uri, method, headers, parms, files);
                }

                public Response sign(Class<?> clazzUse,String strData){
                    byte[] inBuf = Hex.hex2Byte(strData);
                    String rc = (String) XposedHelpers.callStaticMethod(clazzUse, "sign","http://api.izuiyou.com/",inBuf);
                    log("sign = "+rc);
                    return newFixedLengthResponse(rc);

                }

                public Response aesenc(Class<?> clazzUse,String strData){
                    byte[] inBuf = strData.getBytes() ;
                    byte[] rc = (byte[])XposedHelpers.callStaticMethod(clazzUse, "encodeAES",inBuf);
                    String rcStr = Hex.byte2Hex(rc);
                    log("aesenc = "+  rcStr);
                    return newFixedLengthResponse(rcStr);

                }

                public Response aesdec(Class<?> clazzUse,String strData){
                    byte[] inBuf = Hex.hex2Byte(strData);
                    byte[] rc = (byte[])XposedHelpers.callStaticMethod(clazzUse, "decodeAES",inBuf,true);
                    String rcStr = Hex.byte2Hex(rc);
                    log("aesdec = "+  rcStr);
                    return newFixedLengthResponse(rcStr);

                }


                public Response setkey(Class<?> clazzUse,String strKey){
                    XposedHelpers.callStaticMethod(clazzUse, "setProtocolKey",strKey);
                    log("setkey = "+strKey);
                    return newFixedLengthResponse("set key ok");
                }

                public Response getKey(Class<?> clazzUse){
                    String rc = (String) XposedHelpers.callStaticMethod(clazzUse, "getProtocolKey");
                    log("getkey = "+rc);
                    return newFixedLengthResponse(rc);
                }

            }

            new myHttpServer();

        }
    }
}