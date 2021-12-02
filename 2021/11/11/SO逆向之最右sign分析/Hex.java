package com.example.onejanexposed;

public class Hex {
    private final static String PARTEN = "0x|0X|[\\sG-Zg-z,.:;| ?!@#$%^&*/\\()<>+=_-]+";
    private final static String HEX = "0123456789ABCDEF";
    private final static byte[] hex = HEX.getBytes();
    public static String byte2Hex(byte b){
        byte[] buf = new byte[2];
        buf[0] = hex[(b>>4)&0x0f];
        buf[1] = hex[(b>>0)&0x0f];
        return "0x"+new String(buf);
    }
    public static String byte2Hex(byte[] b) {
        if(b ==null) return "";
        byte[] buff = new byte[2 * b.length];
        for (int i = 0; i < b.length; i++) {
            buff[2 * i] = hex[(b[i] >> 4) & 0x0f];
            buff[2 * i + 1] = hex[b[i] & 0x0f];
        }
        // return "0x"+new String(buff);
        return new String(buff);
    }

    public static byte[] hex2Byte(String hex) {
        if(hex==null) return null;
        int index = hex.indexOf(';');
        if(index>=0){
            hex = hex.substring(0,index);
        }
        hex = hex.toUpperCase().replaceAll(PARTEN,"");
        if(hex.length()==0) return null;

        int len = hex.length() / 2;
        byte[] result = new byte[len];
        char[] achar = hex.toCharArray();
        for (int i = 0; i < len; i++) {
            int pos = i * 2;
            result[i] = (byte) (HEX.indexOf(achar[pos]) << 4
                                | HEX.indexOf(achar[pos + 1]));
        }
        return result;
    }
}
