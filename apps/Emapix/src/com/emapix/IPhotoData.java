package com.emapix;

public interface IPhotoData {
    abstract boolean setResource(int index, String resource);
    abstract ResourceImage get(int index);
    abstract ResourceImage [] getAll();
    abstract ResourceImage add(int lat, int lon);
    abstract boolean remove(int index);
    abstract boolean isEmpty(int index);
    abstract int size();
}