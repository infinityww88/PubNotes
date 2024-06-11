# AES

AES(Advanced Encryption Standard)，又称 Rijndael 加密算法，是一种区块加密算法，用来代替之前的 DES，已经被多方分析且为世界广泛使用，已然称为对称密钥加密算法中流行的算法之一。

该算法为比利时密码学家Joan Daemen和Vincent Rijmen所设计，结合两位作者的名字，以Rijndael为名投稿高级加密标准的甄选流程。

严格地说，AES和Rijndael加密法并不完全一样（虽然在实际应用中两者可以互换），因为Rijndael加密法可以支持更大范围的区块和密钥长度：AES的区块长度固定为128比特，密钥长度则可以是128，192或256比特；而Rijndael使用的密钥和区块长度均可以是128，192或256比特。加密过程中使用的密钥是由Rijndael密钥生成方案产生。

截至2006年，针对AES唯一的成功攻击是旁道攻击或社会工程学攻击。美国国家安全局审核了所有的参与竞选AES的最终入围者（包括Rijndael），认为他们均能够满足美国政府传递非机密文件的安全需要。2003年6月，美国政府宣布AES可以用于加密机密文件。

这标志着，由美国国家安全局NSA批准在最高机密信息上使用的加密系统首次可以被公开使用。许多大众化产品只使用128位密钥当作默认值；由于最高机密文件的加密系统必须保证数十年以上的安全性，故推测NSA可能认为128位太短，才以更长的密钥长度为最高机密的加密保留了安全空间。

AES 有两种最常用的加密模式：ECB 和 CBC，区别是 ECB 不需要 IV 偏移量，CBC 需要一个 IV 偏移量，CBC 比 EBC 提供了更多的安全性。

CBC 加密需要一个密钥和 IV 偏移量，它们都是 bytes 类型，并且：

- 密钥必须为 16 字节整数倍的字节类型数据
- 明文必须为 16 字节整数倍的字节类型数据，如果不足需要补全

## Python

Python 需要安装 pycryptodome 以使用 AES 加密：


```sh
python -m pip install pycryptodome
```

```py
from Crypto.Cipher import AES

with open("aes_key.bytes", "rb") as f:
    key = f.read()

with open("aes_iv.bytes", "rb") as f:
    iv = f.read()

aes = AES.new(key, AES.MODE_CBC, iv)

data = b"create a byte of give integer size"
size = (len(data) + 15)//16 * 16
data = data.ljust(size, b'\x00')

data = aes.encrypt(data)

with open("data.bytes", "wb") as f:
    f.write(data)

```

- 在 Python 中进行 AES 加密解密，所传入的密文、明文、秘钥、iv偏移量、都需要是 bytes
- 当秘钥，iv偏移量，待加密的明文，字节长度不够 16 字节或者 16 字节倍数的时候需要进行补全
- CBC 模式j解密需要重新生成 AES 对象，否则会报错 TypeError: decrypt() cannot be called after encrypt()
- 如果加密的数据是字符串，需要先 encode 为 bytes 数据

## C#

AES 在 .NET Library System.Security.Cryptography 中。

```C#
using System.Security.Cryptography;

public class AesTest {

    public static System.ValueTuple<byte[], byte[]> GenerateAesKeyIV() {
		using (Aes myAes = Aes.Create()) {
			myAes.GenerateIV();
			myAes.GenerateKey();
			return System.ValueTuple.Create(myAes.Key, myAes.IV);
		}
	}
	
	public static byte[] Encrypt(string text, byte[] key, byte[] iv) {
		MemoryStream input = new MemoryStream(System.Text.Encoding.UTF8.GetBytes(text));
		MemoryStream output = new MemoryStream();
		using (Aes myAes = Aes.Create()) {
			myAes.Key = key;
			myAes.IV = iv;
			ICryptoTransform encryptor = myAes.CreateEncryptor();
			using (CryptoStream cs = new CryptoStream(output, encryptor, CryptoStreamMode.Write)) {
				input.CopyTo(cs);
			}
		}
		return output.ToArray();
	}
	
	public static string Decrypt(byte[] data, byte[] key, byte[] iv) {
		MemoryStream input = new MemoryStream(data);
		MemoryStream output = new MemoryStream();
		using (AesManaged myAes = new AesManaged()) {
			myAes.Key = key;
			myAes.IV = iv;
			ICryptoTransform decryptor = myAes.CreateDecryptor();
			using (CryptoStream cs = new CryptoStream(input, decryptor, CryptoStreamMode.Read)) {
				cs.CopyTo(output);
			}
		}
		return System.Text.Encoding.UTF8.GetString(output.ToArray());
	}
}
```

AesManaged.GenerateIV/GenerateKey 可以自动生成 key 和 iv。key 和 iv 既可以自动生成，也可以手动指定，只要加密解密两边一样即可。

使用 CBC 模式，需要显示指定 AesManaged.Mode = CipherMode.CBC。AES 是区块加密，两边必须使用一样的区块。但是 python 端使用的是 byte 单位（16），而 C# 端使用的是 bit 单位（128）。

根据 ChatGPT，AES 算法支持 3 种不同的密钥长度：

- AES-128：16 字节，128 位
- AES-192：24 字节，192 位
- AES-256：32 字节，256 位

IV（初始化向量）

AES的IV长度取决于使用的加密模式，但对于常见的块密码模式如CBC（Cipher Block Chaining）和CFB（Cipher Feedback），IV长度通常是一个块的长度，即 16字节（128位）

IV的长度与AES的块大小一致，而AES的块大小固定为128位（16字节），不论使用的密钥长度如何。

AES（Advanced Encryption Standard）的块大小是固定的，为128位（16字节）。不论使用的密钥长度（128位、192位或256位）如何，AES的块大小始终保持128位。这是AES算法的一个基本特性。

AES是一种分组加密算法，它对固定长度的块（128位，即16字节）进行加密。为了确保每个要加密的数据块都具有正确的长度，如果明文数据的长度不是块大小的整数倍，就需要进行填充。以下是填充的原因和常见的填充方式：

- 固定块大小：AES只能处理固定大小的数据块（16字节）。如果数据块的长度不是16字节，就无法直接进行加密操作。
- 保证数据完整性：填充确保加密后的数据可以正确解密，并能还原到原始的明文数据。如果不进行填充，解密后的数据可能会缺失，导致数据不完整。

填充模式：

- PKCS#7 填充：在数据的末尾添加若干个字节，每个字节的值等于添加的字节数
- ANSI X.923 填充：在数据的末尾添加若干个字节，填充值为0，最后一个字节表示填充的字节数
- ISO 10126 填充：在数据的末尾添加若干个随机字节，最后一个字节表示填充的字节数
- Zero Padding（零填充）：在数据的末尾添加若干个0字节

0 填充方法在数据长度刚好是块大小整数倍时需要特殊处理，因为无法区分填充的0和原始数据中的0。它现简单，但通常不推荐用于加密算法，除非数据长度固定或有特殊处理。

```
AES-128
安全性：AES-128被认为是相当安全的，广泛用于各种应用和标准（如TLS/SSL、VPN等）。
破解难度：假设使用最先进的技术进行暴力破解（即尝试所有可能的密钥组合），需要尝试的组合数为 2^128。即使使用当前最强的超级计算机，暴力破解AES-128也是不现实的，可能需要数十亿年。

AES-192
安全性：AES-192提供更高的安全性，比AES-128更难破解。
破解难度：需要尝试的组合数为 2^192。这比AES-128多了很多个数量级，理论上破解它需要的时间比AES-128要长得多。

AES-256
安全性：AES-256提供最高级别的安全性，通常用于需要极高安全性的环境中（如政府和军用）。
破解难度：需要尝试的组合数为 2^256。破解AES-256需要的时间比AES-192还要长很多个数量级，几乎不可能在可预见的未来内完成。

具体破解时间估算
实际破解AES加密的时间依赖于很多因素，包括可用计算能力、算法改进以及潜在的物理攻击（如量子计算）。目前的一些估计如下：

传统计算机：使用目前最先进的传统计算机，对AES-128进行暴力破解的时间可能需要数十亿年甚至更久。
量子计算机：量子计算机使用Grover算法可以将密钥空间的搜索复杂度从 2^n 减少到 2^(n/2)
 。因此，对于AES-128，量子计算机的破解复杂度变为 2^64，对于AES-256，复杂度变为 2^128。尽管如此，目前的量子计算技术还远未达到能够实际破解AES-128或更高级别密钥的能力。

总结
AES-128：非常安全，破解难度极高，但理论上可能在远未来的某些量子计算机上被破解。
AES-192：比AES-128更安全，破解难度更高。
AES-256：目前提供最高级别的安全性，几乎无法在可预见的未来内破解。
在实际应用中，选择密钥长度通常取决于具体的安全需求和性能考虑。对于大多数应用，AES-128已经足够安全。对于需要更高安全性的环境，可以选择AES-256。
```

C# 生成 key 默认是 32 字节（256 位）的，即最高安全级别。如果使用其他长度的 key，可以手动生成。C# 中的 0 填充解密时不会自动移除结尾的 0 字节，必须手动移除。因为填充是在加密前的初始数据上进行的，它本身就可能包括字节 0。解密后，没有明确的信息知道哪些 0 是填充的，哪些是初始数据的，因此交给应用程序自己处理，算法不会移除它们。

要自动移除，使用其他的填充模式。其他的填充模式之所以可以知道移除哪些字节，是因为它们的最后一个字节都指示了填充数据的长度。最常用的是 PKCS7. 但是注意，当初始数据正好是 block 的整数倍的时候，必须填充一个完整的 block，因为必须存在最后一个字节来指示填充数据的长度。

Python 中没有提供 Padding 方法，需要自己实现。下面是 PKCS7 的实现：

```py
BS = AES.block_size # 16
pad = lambda s: s + (BS - len(s) % BS) * bytes([BS - len(s) % BS])
```

注意 BS - len(s) % BS 保证了即使数据是 block 的整数倍，也会填充一个新的 block。



