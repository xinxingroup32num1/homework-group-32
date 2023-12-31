#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <array>

#define ROL32(x, n) ((x) << (n) | (x) >> (32 - (n)))
#define P0(x) ((x) ^ ROL32(x, 9) ^ ROL32(x, 17))
#define P1(x) ((x) ^ ROL32(x, 15) ^ ROL32(x, 23))
#define FF00(x, y, z) ((x) ^ (y) ^ (z))
#define GG00(x, y, z) ((x) ^ (y) ^ (z))
#define FF10(x, y, z) ((x) & (y) | (x) & (z) | (y) & (z))
#define GG10(x, y, z) ((z) ^ ((x) & ((y) ^ (z))))

class SM3 {
	static constexpr uint32_t TT00 = 0x79cc4519;
	static constexpr uint32_t TT10 = 0x7a879d8a;
	static void compress(uint32_t *rec, uint8_t const *blk) {
		uint32_t W[68];
		for (int j = 0; j < 16; j++) {
			W[j] = blk[j << 2] << 030 | blk[j << 2 | 1] << 020 | blk[j << 2 | 2] << 010 | blk[j << 2 | 3];
		}
		for (int j = 16; j < 68; j++) {
			uint32_t TT0 = W[j - 16] ^ W[j - 9] ^ ROL32(W[j - 3], 15);
			W[j] = P1(TT0) ^ W[j - 6] ^ ROL32(W[j - 13], 7);
		}
		uint32_t A = rec[0];
		uint32_t B = rec[1];
		uint32_t C = rec[2];
		uint32_t D = rec[3];
		uint32_t E = rec[4];
		uint32_t F = rec[5];
		uint32_t G = rec[6];
		uint32_t H = rec[7];
		for (int j = 0; j < 16; j++) {
			uint32_t A12 = ROL32(A, 12);
			uint32_t AEK = A12 + E + K[j];
			uint32_t SS1 = ROL32(AEK, 7);
			uint32_t TT1 = FF00(A, B, C) + D + (SS1 ^ A12) + (W[j] ^ W[j + 4]);
			uint32_t TT2 = GG00(E, F, G) + H + SS1 + W[j];
			D = C;
			C = ROL32(B, 9);
			B = A;
			A = TT1;
			H = G;
			G = ROL32(F, 19);
			F = E;
			E = P0(TT2);
		}
		for (int j = 16; j < 64; j++) {
			uint32_t A12 = ROL32(A, 12);
			uint32_t AEK = A12 + E + K[j];
			uint32_t SS1 = ROL32(AEK, 7);
			uint32_t TT1 = FF10(A, B, C) + D + (SS1 ^ A12) + (W[j] ^ W[j + 4]);
			uint32_t TT2 = GG10(E, F, G) + H + SS1 + W[j];
			D = C;
			C = ROL32(B, 9);
			B = A;
			A = TT1;
			H = G;
			G = ROL32(F, 19);
			F = E;
			E = P0(TT2);
		}
		rec[0] ^= A;
		rec[1] ^= B;
		rec[2] ^= C;
		rec[3] ^= D;
		rec[4] ^= E;
		rec[5] ^= F;
		rec[6] ^= G;
		rec[7] ^= H;
	}
public:
	uint64_t countr = 0;
	uint32_t rec[8] = {
		0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
		0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
	};
	void join(uint8_t const* blk) {
		compress(rec, blk);
		countr += 512;
	}
	void join_last(uint8_t const *fin, size_t len, uint8_t *buf) const {
		uint8_t blk[64];
		memcpy(blk, fin, len);
		memset(blk + len, 0, 64 - len);
		blk[len] = 0x80;
		uint32_t rectmp[8];
		memcpy(rectmp, rec, 32);
		uint64_t ctrtmp = countr + 8 * len;
		uint8_t *u8ctmp = (uint8_t *)&ctrtmp;
		if (len >= 56) {
			compress(rectmp, blk);
			memset(blk, 0, 56);
		}
		blk[63] = u8ctmp[0];
		blk[62] = u8ctmp[1];
		blk[61] = u8ctmp[2];
		blk[60] = u8ctmp[3];
		blk[59] = u8ctmp[4];
		blk[58] = u8ctmp[5];
		blk[57] = u8ctmp[6];
		blk[56] = u8ctmp[7];
		compress(rectmp, blk);
		for (int j = 0; j < 8; j++) {
			buf[j << 2] = rectmp[j] >> 030;
			buf[j << 2 | 1] = rectmp[j] >> 020;
			buf[j << 2 | 2] = rectmp[j] >> 010;
			buf[j << 2 | 3] = rectmp[j];
		}
	}
	static const std::array<uint32_t, 64> K;
};
const std::array<uint32_t, 64> SM3::K = []() {
	std::array<uint32_t, 64> K = {};
	for (int j = 0; j < 16; j++) {
		K[j] = SM3::TT00 << j % 32 | SM3::TT00 >> (32 - j) % 32;
	}
	for (int j = 16; j < 64; j++) {
		K[j] = SM3::TT10 << j % 32 | SM3::TT10 >> (96 - j) % 32;
	}
	return K;
}();

inline void SM3_calc(uint8_t const *data, size_t len, uint8_t *buf, SM3 sm3 = SM3()) {
	size_t n = len - len % 64;
	for (size_t i = 0; i < n; i += 64) {
		sm3.join(data + i);
	}
	sm3.join_last(data + n, len % 64, buf);
}
inline void print_digest(uint8_t const *data, size_t len) {
	for (int i = 0;;) {
		printf("%02X", data[i]);
		if (++i < len) {
			printf(" ");
		} else {
			printf("\n");
			break;
		}
	}
}