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

AesManaged.GenerateIV/GenerateKey 可以自动生成 key 和 iv。key 和 iv 既可以自动生成，也可以手动指定，只要加密解密两边一样即可。

使用 CBC 模式，需要显示指定 AesManaged.Mode = CipherMode.CBC。AES 是区块加密，两边必须使用一样的区块。但是 python 端使用的是 byte 单位（16），而 C# 端使用的是 bit 单位（128）。另外 C# 端还要指定 padding（PaddingMode.Zeros）。

```C#
using System.Security.Cryptography;

public class AesTest {

    public static System.ValueTuple<byte[], byte[]> GenerateAesKeyIV() {
		using (AesManaged myAes = new AesManaged()) {
			myAes.GenerateIV();
			myAes.GenerateKey();
			return System.ValueTuple.Create(myAes.Key, myAes.IV);
		}
	}
	
	public static byte[] Encrypt(string text, byte[] key, byte[] iv) {
		MemoryStream input = new MemoryStream(System.Text.Encoding.UTF8.GetBytes(text));
		MemoryStream output = new MemoryStream();
		using (AesManaged myAes = new AesManaged()) {
			myAes.Mode = CipherMode.CBC;
			myAes.BlockSize = 128;
			myAes.Padding = PaddingMode.Zeros;
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
			myAes.Mode = CipherMode.CBC;
			myAes.BlockSize = 128;
			myAes.Padding = PaddingMode.Zeros;
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
