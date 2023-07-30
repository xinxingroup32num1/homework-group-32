#include <iostream>
#include <chrono> // for measuring time
#include "sm4.h"
using namespace std;
using namespace std::chrono; // for measuring time
//���ֽ�����ת����unsigned long
void tolong(unsigned char* in, unsigned long* out)
{
	int i = 0;
	*out = 0;
	for (i = 0; i < 4; i++)
	{
		*out = ((unsigned long)in[i] << (24 - i * 8)) ^ *out;
	}
}
//unsigned longת�������ֽ�����
void longto(unsigned long in, unsigned char* out)
{
	for (int i = 0; i < 4; i++)
		*(out + i) = (unsigned long)(in >> (24 - i * 8));
}
//���ƣ���������λ
unsigned long leftmove(unsigned long data, int length)
{
	unsigned long result = 0;
	result = (data << length) ^ (data >> (32 - length));
	return result;
}
unsigned long lunkey(unsigned long input)                 //��ʹ��Sbox���з����Ա仯�������
{
	unsigned long temp = 0;
	unsigned char inbox[4] = { 0 };
	unsigned char outbox[4] = { 0 };
	longto(input, inbox);
	for (int i = 0; i < 4; i++)
		outbox[i] = TBL_SBOX[inbox[i]];
	tolong(outbox, &temp);
	temp = temp ^ leftmove(temp, 13) ^ leftmove(temp, 23);
	return temp;
}
//��ʹ��Sbox���з����Ա仯���ٽ������
unsigned long lundata(unsigned long input)
{
	unsigned long temp = 0;
	unsigned char inbox[4] = { 0 };
	unsigned char outbox[4] = { 0 };
	longto(input, inbox);
	for (int i = 0; i < 4; i++)
		outbox[i] = TBL_SBOX[inbox[i]];
	tolong(outbox, &temp);
	temp = temp ^ leftmove(temp, 2) ^ leftmove(temp, 10) ^ leftmove(temp, 18) ^ leftmove(temp, 24);
	return temp;
}

void encode(int len, unsigned char* key, unsigned char* input, unsigned char* output)   //���ܺ���
{
	int i = 0;
	int j = 0;
	unsigned long keyarr[4] = { 0 };//�洢��Կ������
	unsigned long keylist[36] = { 0 };//��Կ��չ����Ľ��
	unsigned long datalist[36] = { 0 };//��������
	tolong(key, &(keyarr[0]));
	tolong(key + 4, &(keyarr[1]));
	tolong(key + 8, &(keyarr[2]));
	tolong(key + 12, &(keyarr[3]));
	//��һ������Կ��ϵͳ���������
	keylist[0] = keyarr[0] ^ TBL_SYS_PARAMS[0];
	keylist[1] = keyarr[1] ^ TBL_SYS_PARAMS[1];
	keylist[2] = keyarr[2] ^ TBL_SYS_PARAMS[2];
	keylist[3] = keyarr[3] ^ TBL_SYS_PARAMS[3];
	//�ڶ�������ȡ����Կ
	for (i = 0; i < 32; i++)
	{
		keylist[i + 4] = keylist[i] ^ lunkey(keylist[i + 1] ^ keylist[i + 2] ^ keylist[i + 3] ^ TBL_FIX_PARAMS[i]);
	}
	//�����벹���16�ı���
	/*unsigned char* input16 = (unsigned char*)malloc(40);
	for (int i = 0; i < len; i++)
		*(input16 + i) = *(input + i);*/
		/*for (int i = 0; i < 16 - len % 16; i++)
			*(input16 + len + i) = 0;*/
	for (j = 0; j < len / 16; j++)
	{
		tolong(input + 16 * j, &datalist[0]);
		tolong(input + 16 * j + 4, &datalist[1]);
		tolong(input + 16 * j + 8, &datalist[2]);
		tolong(input + 16 * j + 12, &datalist[3]);
		//����
		for (i = 0; i < 32; i++)
			datalist[i + 4] = datalist[i] ^ lundata(datalist[i + 1] ^ datalist[i + 2] ^ datalist[i + 3] ^ keylist[4 + i]);
		//
		longto(datalist[35], output + 16 * j);
		longto(datalist[34], output + 16 * j + 4);
		longto(datalist[33], output + 16 * j + 8);
		longto(datalist[32], output + 16 * j + 12);
	}/*
	free(input16);*/
}

int main()
{
	unsigned char encrypt[50] = { 0 };    //����������������
	unsigned char key[16] = { 0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10 };
	//����16�ֽڵ���Կ
	//����32�ֽڵ�ԭʼ��������
	unsigned char Data_plain[16] = { 0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10 };
	int len = 16 * (sizeof(Data_plain) / 16) + 16 * ((sizeof(Data_plain) % 16) ? 1 : 0);//�õ��������ֽ���
	auto start = high_resolution_clock::now(); // ��¼��ʼʱ��
	encode(sizeof(Data_plain), key, Data_plain, encrypt);            //���ݼ���
	auto stop = high_resolution_clock::now(); // ��¼����ʱ��
	printf("���ܺ������ǣ�\n");
	for (int i = 0; i < len; i++)
		printf("%x ", *(encrypt + i));
	printf("\n");

	// �������ʱ�䲢���
	auto duration = duration_cast<microseconds>(stop - start);
	cout << "���ܲ�����ʱ�� " << duration.count() << " ΢��" << endl;

	return 0;
}