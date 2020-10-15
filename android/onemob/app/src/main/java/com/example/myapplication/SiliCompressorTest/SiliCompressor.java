package com.example.myapplication.SiliCompressorTest;

import android.content.Context;

import androidx.annotation.NonNull;

import com.iceteck.silicompressorr.CompressionException;

public class SiliCompressor extends com.iceteck.silicompressorr.SiliCompressor {

    public SiliCompressor(Context context) {
        super(context);
    }

    @Override
    public String compressVideo(@NonNull String videoFilePath, @NonNull String destinationDir) throws CompressionException {
        return super.compressVideo(videoFilePath, destinationDir);
    }
}
