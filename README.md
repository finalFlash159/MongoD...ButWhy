### What is MongoDB Atlas?
MongoDB is a document-oriented database. Simply put, you get the scalability and flexibility you want, with the querying and indexing features you need.

```python
# Connect to MongoDB instance running on localhost
client = pymongo.MongoClient()                   

# Access the 'restaurants' collection
# in the 'test' database
collection = client.test.restaurants
```

## MongoDB Database

### Documents

MongoDB stores data records as BSON documents. BSON is a binary representation of JSON documents, though it contains more data types than JSON. For the BSON spec, see bsonspec.org. See also BSON Types.
![](https://www.mongodb.com/docs/manual/images/crud-annotated-document.svg)

### Document Structure
```json
{
   field1: value1,
   field2: value2,
   field3: value3,
   ...
   fieldN: valueN
}
```

The value of a field can be any of the BSON data types, including other documents, arrays, and arrays of documents. For example, the following document contains values of varying types:
```json
var mydoc = {
               _id: ObjectId("5099803df3f4948bd2f98391"),
               name: { first: "Alan", last: "Turing" },
               birth: new Date('Jun 23, 1912'),
               death: new Date('Jun 07, 1954'),
               contribs: [ "Turing machine", "Turing test", "Turingery" ],
               views : NumberLong(1250000)
            }
```

- `_id` holds an **ObjectId.**

- `name` holds an embedded document that contains the fields `first` and `last`.

- `birth` and `death` hold values of the **Date type.**

- `contribs` holds an **array of strings.**

- `views` holds a value of the **NumberLong type.**

## BSON Types trong MongoDB

BSON (Binary JSON) là định dạng tuần tự hoá nhị phân được sử dụng để lưu trữ document và thực hiện remote procedure calls trong MongoDB. Bạn có thể tìm hiểu thêm về định nghĩa BSON tại [bsonspec.org](http://bsonspec.org).

Mỗi BSON type có cả định danh kiểu số (integer) và chuỗi (string) như sau:

| Type                  | Number | Alias      | Notes                                               |
|-----------------------|--------|------------|-----------------------------------------------------|
| Double                | 1      | "double"   |                                                     |
| String                | 2      | "string"   |                                                     |
| Object                | 3      | "object"   |                                                     |
| Array                 | 4      | "array"    |                                                     |
| Binary data           | 5      | "binData"  |                                                     |
| Undefined             | 6      | "undefined"| Deprecated.                                         |
| ObjectId              | 7      | "objectId" |                                                     |
| Boolean               | 8      | "bool"     |                                                     |
| Date                  | 9      | "date"     |                                                     |
| Null                  | 10     | "null"     |                                                     |
| Regular Expression    | 11     | "regex"    |                                                     |
| DBPointer             | 12     | "dbPointer"| Deprecated.                                         |
| JavaScript            | 13     | "javascript"|                                                    |
| Symbol                | 14     | "symbol"   | Deprecated.                                         |
| 32-bit integer        | 16     | "int"      |                                                     |
| Timestamp             | 17     | "timestamp"|                                                     |
| 64-bit integer        | 18     | "long"     |                                                     |
| Decimal128            | 19     | "decimal"  |                                                     |
| Min key               | -1     | "minKey"   |                                                     |
| Max key               | 127    | "maxKey"   |                                                     |

Các toán tử như `$type` (trong query hoặc aggregation) sử dụng các giá trị này để truy vấn các trường theo kiểu BSON của chúng.

---

## Các Loại BSON Đặc Biệt

### 1. Binary Data

- **Giải thích:**  
  BSON binary binData là một mảng byte. Mỗi giá trị binData có một subtype cho biết cách giải thích dữ liệu nhị phân đó.

- **Bảng subtypes của Binary Data:**

  | Number | Description                                  |
  |--------|----------------------------------------------|
  | 0      | Generic binary subtype                       |
  | 1      | Function data                                |
  | 2      | Binary (old)                                 |
  | 3      | UUID (old)                                   |
  | 4      | UUID                                         |
  | 5      | MD5                                          |
  | 6      | Encrypted BSON value                         |
  | 7      | Compressed time series data (New in version 5.2)|
  | 8      | Sensitive data (ví dụ: key, secret). MongoDB không log giá trị thật mà chỉ log placeholder. |
  | 9      | Vector data (dãy số được đóng gói chặt)       |
  | 128    | Custom data                                  |

---

### 2. ObjectId

- **Giải thích:**  
  ObjectId là 12 byte, được thiết kế để tạo ra các giá trị gần như duy nhất, nhanh chóng và có thứ tự tương đối. Cấu trúc của ObjectId gồm:
  - **4 byte**: Timestamp (số giây kể từ Unix epoch).
  - **5 byte**: Giá trị ngẫu nhiên được tạo ra một lần cho mỗi process (đảm bảo tính duy nhất cho máy và process).
  - **3 byte**: Bộ đếm tăng dần, được khởi tạo ngẫu nhiên.

- **Lưu ý:**  
  - Các byte quan trọng nhất (timestamp và counter) được lưu theo thứ tự big-endian, khác với hầu hết các giá trị BSON khác (little-endian).
  - Nếu khởi tạo ObjectId từ một số nguyên, số đó sẽ thay thế timestamp.
  - Mỗi document trong một collection thông thường phải có trường `_id` duy nhất, và nếu thiếu, driver MongoDB sẽ tự động tạo ObjectId.
  - Bạn có thể sử dụng phương thức `ObjectId.getTimestamp()` (trong `mongosh`) để lấy thời gian tạo ObjectId.
  - Mặc dù ObjectIds theo thứ tự xấp xỉ theo thời gian tạo, chúng không đảm bảo thứ tự tuyệt đối vì có độ phân giải chỉ đến giây và do đồng hồ hệ thống có thể không đồng bộ.

---

### 3. String

- **Giải thích:**  
  BSON strings được lưu dưới dạng UTF-8. Điều này có nghĩa là khi chuyển từ string của ngôn ngữ lập trình sang BSON, hầu hết các ký tự quốc tế đều được hỗ trợ.
  - Các truy vấn `$regex` trong MongoDB cũng hỗ trợ chuỗi UTF-8.

---

### 4. Timestamps

- **Giải thích:**  
  BSON có một loại timestamp riêng biệt cho mục đích nội bộ của MongoDB, không liên quan đến kiểu `Date`.  
  - Timestamp BSON là một giá trị 64-bit:
    - **32-bit**: giá trị `time_t` (số giây từ Unix epoch).
    - **32-bit**: số thứ tự tăng dần cho các thao tác trong cùng một giây.
  - Mặc dù BSON là little-endian, `mongod` luôn so sánh phần `time_t` trước khi xét đến số thứ tự, bất kể endianness.
  - Timestamp thường được sử dụng trong replication (ví dụ: trường `ts` trong oplog), và mỗi giá trị trong oplog là duy nhất.

> **Lưu ý:** Thông thường, trong phát triển ứng dụng, bạn sẽ dùng kiểu Date thay vì timestamp BSON.

---

### 5. Date

- **Giải thích:**  
  BSON Date là một số nguyên 64-bit đại diện cho số mili-giây kể từ Unix epoch (1/1/1970).  
  - Cho phép biểu diễn khoảng thời gian rộng, gần 290 triệu năm vào quá khứ và tương lai.
  - BSON Date được coi là UTC datetime.
  - Giá trị Date là số có dấu, nên các giá trị âm biểu diễn thời gian trước năm 1970.
  
**Ví dụ tạo Date trong mongosh:**

```javascript
// Sử dụng new Date()
var mydate1 = new Date();

// Sử dụng ISODate()
var mydate2 = ISODate();
```

#### Field Names
Trong MongoDB, tên field luôn là chuỗi (string) và có một số quy định và giới hạn như sau:

1. **Field `id`:**
   - Field `id` là field đặc biệt dành cho primary key. 
   - Giá trị của `id` phải là duy nhất trong mỗi collection và không được phép thay đổi (immutable).
   - `id` có thể là bất kỳ kiểu dữ liệu nào, ngoại trừ array hoặc regex.
   - Nếu `id` chứa các subfield (trường con), thì tên của các subfield không được bắt đầu bằng ký tự ($).

2. **Giới hạn về ký tự trong tên field:**
   - Tên field không được chứa ký tự null (null character).
   - Mặc dù MongoDB cho phép lưu trữ tên field chứa dấu chấm (`.`) và dấu đô la (`$`), phiên bản MongoDB 5.0 trở đi có hỗ trợ cải tiến cho việc sử dụng (`$`) và (``.``) trong tên field với một số hạn chế nhất định (tham khảo thêm phần Field Name Considerations).

3. **Tính duy nhất của tên field trong một document:**
   - Mỗi tên field trong một document phải là duy nhất. Không được lưu trữ document có tên field trùng lặp.
   - Các thao tác CRUD (create, read, update, delete) của MongoDB có thể hoạt động không như mong muốn nếu document chứa các field trùng lặp.
   - Mặc dù một số thư viện xây dựng BSON có thể cho phép tạo document với các tên field trùng lặp, nhưng việc chèn (insert) những document này vào MongoDB sẽ không được hỗ trợ đầy đủ. Có thể driver sẽ tự động bỏ qua các giá trị trùng lặp hoặc lưu một document không hợp lệ, dẫn đến kết quả truy vấn không nhất quán.
   - Việc cập nhật document có tên field trùng lặp cũng không được hỗ trợ, kể cả khi update có vẻ như thành công.

4. **Kiểm tra trùng lặp tên field:**
   - Từ MongoDB 6.1, bạn có thể sử dụng lệnh `validate` với tùy chọn `full: true` để kiểm tra xem document có chứa tên field trùng lặp không.
   - Ở bất kỳ phiên bản MongoDB nào, bạn có thể sử dụng toán tử aggregation `$objectToArray` để phát hiện xem một document có chứa tên field trùng lặp hay không.


### Dot Notation trong MongoDB

MongoDB sử dụng **dot notation** để truy cập các phần tử của một mảng và để truy cập các trường của một document lồng nhau (embedded document).

#### Arrays (Mảng)

Để chỉ định hoặc truy cập một phần tử trong mảng dựa trên vị trí chỉ số (bắt đầu từ 0), bạn ghép tên mảng với dấu chấm (`.`) và chỉ số phần tử, sau đó đặt trong dấu ngoặc kép:

```json
"<array>.<index>"
```


**Ví dụ:**

Giả sử bạn có một document với trường như sau:

```json
{
  ...
  "contribs": [ "Turing machine", "Turing test", "Turingery" ],
  ...
}
```

- Để truy cập phần tử thứ ba của mảng `contribs`, bạn sử dụng dot notation: `"contribs.2"`.

  

# Quản lý Databases với MongoDB Atlas UI

MongoDB Atlas UI cho phép bạn quản lý các cơ sở dữ liệu và collections trong cluster của mình thông qua giao diện đồ họa. Dưới đây là một số hướng dẫn cơ bản kèm theo vai trò cần thiết:

---

## Vai Trò Cần Thiết

| Hành động            | Vai trò yêu cầu                                                                 |
|----------------------|---------------------------------------------------------------------------------|
| **Tạo Database**     | Một trong các vai trò: Project Owner, Organization Owner, Project Data Access Admin, hoặc Project Data Access Read/Write. |
| **Xem Databases**    | Ít nhất vai trò Project Data Access Read Only.                                  |
| **Xóa Database**     | Một trong các vai trò: Project Owner hoặc Project Data Access Admin.            |

---

## Tạo Cơ Sở Dữ Liệu (Create a Database)

1. **Truy cập Clusters:**
   - Đăng nhập vào Atlas, chọn trang **Clusters** của dự án của bạn.
   - Nếu cần, chọn tổ chức và dự án từ menu **Organizations** và **Projects** trong thanh điều hướng, sau đó nhấp vào **Clusters** ở sidebar.

2. **Truy cập Collections:**
   - Nhấp nút **Browse Collections** cho cluster của bạn để mở **Data Explorer**.

3. **Tạo Database:**
   - Nhấp vào nút **Create Database**.
   - Nhập tên của Database và tên Collection đầu tiên.
   - **Lưu ý:** Không đặt tên chứa thông tin nhạy cảm.
   - Tìm hiểu thêm về [Naming Restrictions](https://docs.mongodb.com/manual/reference/limits/#naming-restrictions).

4. **Tùy Chọn Collection:**
   - **Capped Collection:** Chọn nếu muốn tạo collection với giới hạn kích thước. Sau đó chỉ định kích thước tối đa (byte).
   - **Time Series Collection:** Chọn nếu muốn tạo collection dạng time series, chỉ định time field, granularity, và tùy chọn meta field cũng như thời gian hết hạn cho dữ liệu cũ.

5. **Xác Nhận:**
   - Nhấp **Create**. Sau khi tạo thành công, Database cùng với Collection đầu tiên sẽ hiển thị trong Atlas UI.

---

## Xem Cơ Sở Dữ Liệu (View Databases)

1. **Truy cập Clusters:**
   - Đăng nhập Atlas, chọn trang **Clusters** của dự án.

2. **Truy cập Collections:**
   - Nhấp vào **Browse Collections** cho cluster của bạn để mở **Data Explorer**.
   - Tại đây, bạn có thể xem danh sách các databases và collections hiện có.

3. **Visualize Database Data:**
   - Để trực quan hóa dữ liệu, nhấp vào nút **Visualize Your Data** khi xem một database hoặc collection cụ thể.
   - Atlas sẽ mở MongoDB Charts, nơi bạn có thể xây dựng biểu đồ từ data source đã chọn. Tham khảo [Build Charts](https://docs.mongodb.com/charts/) để biết chi tiết.

---

## Xóa Cơ Sở Dữ Liệu (Drop a Database)

1. **Xóa Database:**
   - Trong Atlas UI, chọn hoặc di chuột qua Database cần xóa.
   - Nhấp vào biểu tượng thùng rác (trash can) của Database đó.

2. **Xác Nhận Hành Động:**
   - Gõ tên Database để xác nhận việc xóa.
   - Nhấp vào **Drop** để hoàn tất.

---
# Embedded Documents trong MongoDB

## Embedded Documents là gì?

Trong cơ sở dữ liệu quan hệ, bạn lưu trữ từng thực thể riêng biệt trong các bảng riêng và liên kết chúng với nhau thông qua các khóa ngoại. Mặc dù MongoDB hoàn toàn hỗ trợ tham chiếu từ document này sang document khác và thậm chí là join nhiều document, nhưng sẽ là sai lầm nếu sử dụng cơ sở dữ liệu document giống như cách bạn sử dụng cơ sở dữ liệu quan hệ.

## Ví dụ về Embedded Documents

Hãy xem xét một cấu trúc đơn giản với một người dùng và địa chỉ của họ.

### Cách tiếp cận sử dụng tham chiếu (references):

```javascript
> db.user.findOne()
{
    _id: 111111,
    email: "email@example.com",
    name: {given: "Jane", family: "Han"},
}

> db.address.find({user_id: 111111})
{
    _id: 121212,
    street: "111 Elm Street",
    city: "Springfield",
    state: "Ohio",
    country: "US",
    zip: "00000"
}
```

### Cách tiếp cận sử dụng embedded document:

```javascript
> db.user.findOne({_id: 111111})
{    
    _id: 111111,    
    email: "email@example.com",    
    name: {given: "Jane", family: "Han"},    
    address: {    
        street: "111 Elm Street",    
        city: "Springfield",    
        state: "Ohio",    
        country: "US",    
        zip: "00000",    
    }    
}
```

Bây giờ, thay vì phải thực hiện một truy vấn riêng biệt đối với collection address để lấy địa chỉ của Jane Han, bạn có thể truy cập nó như một sub-document của bản ghi người dùng.

### Lưu trữ nhiều địa chỉ:

```javascript
> db.user.findOne({_id: 111111})
{    
    _id: 111111,    
    email: "email@example.com",    
    name: {given: "Jane", family: "Han"},    
    addresses: [    
        {    
            label: "Home",    
            street: "111 Elm Street",    
            city: "Springfield",    
            state: "Ohio",    
            country: "US",    
            zip: "00000",    
        },    
        {label: "Work", ...}    
    ]    
}
```

Bạn thậm chí có thể cập nhật các địa chỉ riêng lẻ bằng toán tử vị trí (positional operator):

```javascript
> db.user.update(    
    {_id: 111111,    
    "addresses.label": "Home"},    
    {$set: {"addresses.$.street": "112 Elm Street"}}    
)
```

Lưu ý rằng bạn cần đặt bất kỳ khóa truy vấn hoặc cập nhật nào có chứa dấu chấm (như "addresses.label") trong dấu ngoặc kép để đảm bảo cú pháp chính xác. Phần truy vấn của lệnh update cần bao gồm trường mảng bạn đang cập nhật, và sau đó phần update sẽ áp dụng cho phần tử đầu tiên khớp trong mảng.

## Tại sao (và khi nào) nên ưu tiên nhúng hơn tham chiếu

Embedded documents là một cách hiệu quả và gọn gàng để lưu trữ dữ liệu liên quan, đặc biệt là dữ liệu thường xuyên được truy cập cùng nhau. Nói chung, khi thiết kế schema cho MongoDB, bạn nên ưu tiên nhúng (embedding) theo mặc định và chỉ sử dụng tham chiếu (references) và join ở phía ứng dụng hoặc cơ sở dữ liệu khi chúng thực sự cần thiết. Workload càng thường xuyên có thể truy xuất một document duy nhất và có tất cả dữ liệu cần thiết, hiệu suất ứng dụng của bạn sẽ càng ổn định và cao.

## Các mẫu nhúng phổ biến

### 1. Embedded Document Pattern

Đây là mẫu chung về việc ưu tiên nhúng ngay cả các cấu trúc phụ phức tạp vào các documents mà chúng được sử dụng cùng. Quy tắc điển hình là:

**"Những gì bạn sử dụng cùng nhau, hãy lưu trữ cùng nhau."**

### 2. Embedded Subset Pattern

Một trường hợp kết hợp, mẫu subset xuất hiện khi bạn có một collection riêng biệt cho một danh sách các item liên quan có thể rất dài, nhưng bạn muốn giữ một số item đó dễ dàng để hiển thị cho người dùng. Ví dụ:

```javascript
> db.movie.findOne()
{    
    _id: 333333,    
    title: "The Big Lebowski"
}
        
> db.review.find({movie_id: 333333})
{    
    _id: 454545,    
    movie_id: 333333,    
    stars: 3,    
    text: "it was OK"    
}    
{    
    _id: 565656,    
    movie_id: 333333,    
    stars: 5,    
    text: "the best"    
}    
...
```

Bây giờ hãy tưởng tượng bạn có hàng nghìn đánh giá, nhưng bạn luôn hiển thị hai đánh giá gần đây nhất khi hiển thị một bộ phim. Trong trường hợp này, việc lưu trữ tập con đó dưới dạng danh sách trong document movie là hợp lý.

```javascript
> db.movie.findOne({_id: 333333})
{    
    _id: 333333,    
    title: "The Big Lebowski",    
    recent_reviews: [    
        {_id: 454545, stars: 3, text: "it was OK"},    
        {_id: 565656, stars: 5, text: "the best"}    
    ]    
}
```

**Nếu bạn thường xuyên truy cập một tập con của các item liên quan, hãy nhúng tập con đó.**

### 3. Extended Reference Pattern

Một trường hợp kết hợp khác được gọi là Extended Reference. Nó khá giống với Subset Pattern, ở chỗ nó tối ưu hóa cho một lượng nhỏ thông tin thường xuyên được truy cập để lưu trữ trên document nơi nó cần. Trong trường hợp này, thay vì một danh sách, nó được sử dụng khi một document tham chiếu đến document khác trong collection riêng, nhưng cũng lưu trữ một số trường từ document khác đó để dễ truy cập.

Ví dụ:

```javascript
> db.movie.findOne({_id: 444444})
{    
    _id: 444444,    
    title: "One Flew Over the Cuckoo's Nest",    
    studio_id: 999999,    
    studio_name: "Fantasy Films"    
}
```

Như bạn có thể thấy, `studio_id` được lưu trữ để bạn có thể tra cứu thêm thông tin về studio sản xuất phim, nhưng tên của studio cũng được sao chép vào document này để dễ hiển thị. Lưu ý rằng nếu bạn đang nhúng thông tin từ các document thay đổi thường xuyên, bạn cần nhớ cập nhật các document nơi bạn đã sao chép thông tin đó khi nó thay đổi.

**Nếu bạn thường xuyên truy cập một vài trường từ document được tham chiếu, hãy nhúng các trường đó.**

## Khi nào không nên sử dụng Embedded Documents

### 1. Danh sách không giới hạn (Unbounded Lists)

Lưu trữ các danh sách ngắn thông tin liên quan trong document mà chúng thuộc về rất hợp lý, nhưng nếu danh sách của bạn có thể phát triển không kiểm soát, đặt nó trong một document duy nhất không chỉ không khôn ngoan mà còn không khả thi! MongoDB có giới hạn về kích thước của một document duy nhất, và nếu document được truy cập thường xuyên, bạn sẽ bắt đầu thấy tác động tiêu cực từ việc sử dụng bộ nhớ quá mức.

**Nếu một danh sách có thể phát triển không giới hạn, hãy đặt nó trong collection riêng.**

### 2. Truy cập độc lập (Independent Access)

Một thời điểm khác bạn nên lưu trữ sub-documents trong collection riêng là khi bạn muốn truy cập chúng độc lập với document cha mà bạn lẽ ra sẽ đặt chúng vào. Ví dụ, xem xét một sản phẩm được sản xuất bởi một công ty. Nếu công ty chỉ bán một số ít sản phẩm, bạn có thể muốn lưu trữ chúng như một phần của document công ty. Tuy nhiên, nếu bạn muốn truy cập trực tiếp các sản phẩm đó theo SKU, hoặc tái sử dụng chúng trên nhiều công ty, bạn sẽ muốn lưu trữ chúng trong collection riêng.

# Data Modeling trong MongoDB

## Data Modeling là gì?

Data modeling là việc tổ chức dữ liệu trong cơ sở dữ liệu và thiết lập các liên kết giữa các thực thể liên quan. Dữ liệu trong MongoDB có mô hình schema linh hoạt, điều này có nghĩa là:

- Documents trong cùng một collection không bắt buộc phải có cùng một tập hợp các trường.
- Kiểu dữ liệu của một trường có thể khác nhau giữa các documents trong cùng một collection.
- Nhìn chung, các documents trong một collection thường có cấu trúc tương tự. Để đảm bảo tính nhất quán trong mô hình dữ liệu của bạn, bạn có thể tạo các quy tắc schema validation.

## Các trường hợp sử dụng

Mô hình dữ liệu linh hoạt cho phép bạn tổ chức dữ liệu phù hợp với nhu cầu của ứng dụng. MongoDB là cơ sở dữ liệu document, nghĩa là bạn có thể nhúng dữ liệu liên quan vào các trường đối tượng và mảng.

Schema linh hoạt hữu ích trong các kịch bản sau:

- Công ty của bạn theo dõi nhân viên làm việc ở phòng ban nào. Bạn có thể nhúng thông tin phòng ban bên trong collection nhân viên để trả về thông tin liên quan trong một truy vấn duy nhất.

- Ứng dụng thương mại điện tử của bạn hiển thị năm đánh giá gần đây nhất khi hiển thị sản phẩm. Bạn có thể lưu trữ các đánh giá gần đây trong cùng collection với dữ liệu sản phẩm, và lưu trữ các đánh giá cũ hơn trong collection riêng biệt vì các đánh giá cũ không được truy cập thường xuyên.

- Cửa hàng quần áo của bạn cần tạo ứng dụng một trang cho danh mục sản phẩm. Các sản phẩm khác nhau có các thuộc tính khác nhau và do đó sử dụng các trường document khác nhau. Tuy nhiên, bạn có thể lưu trữ tất cả các sản phẩm trong cùng một collection.

## Thiết kế Schema: Sự khác biệt giữa cơ sở dữ liệu quan hệ và document

Khi thiết kế schema cho cơ sở dữ liệu document như MongoDB, có một số điểm khác biệt quan trọng so với cơ sở dữ liệu quan hệ:

| Cơ sở dữ liệu quan hệ | Cơ sở dữ liệu document |
|------------------------|------------------------|
| Bạn phải xác định schema của bảng trước khi chèn dữ liệu. | Schema của bạn có thể thay đổi theo thời gian khi nhu cầu của ứng dụng thay đổi. |
| Bạn thường cần join dữ liệu từ nhiều bảng khác nhau để trả về dữ liệu cần thiết cho ứng dụng. | Mô hình dữ liệu linh hoạt cho phép bạn lưu trữ dữ liệu để phù hợp với cách ứng dụng trả về dữ liệu và tránh joins. Việc tránh joins qua nhiều collections cải thiện hiệu suất và giảm tải cho triển khai của bạn. |

## Lên kế hoạch Schema

Để đảm bảo mô hình dữ liệu của bạn có cấu trúc logic và đạt hiệu suất tối ưu, hãy lên kế hoạch schema trước khi sử dụng cơ sở dữ liệu ở quy mô sản xuất. Để xác định mô hình dữ liệu, hãy sử dụng quy trình thiết kế schema sau:

1. Xác định khối lượng công việc của ứng dụng.
2. Xác định mối quan hệ giữa các đối tượng trong các collections.
3. Áp dụng các mẫu thiết kế.

## Liên kết dữ liệu liên quan

Khi thiết kế mô hình dữ liệu trong MongoDB, hãy xem xét cấu trúc của các documents và cách ứng dụng sử dụng dữ liệu từ các thực thể liên quan.

Để liên kết dữ liệu liên quan, bạn có thể:

- Nhúng dữ liệu liên quan trong một document duy nhất.
- Lưu trữ dữ liệu liên quan trong collection riêng biệt và truy cập bằng tham chiếu.

### Dữ liệu nhúng (Embedded Data)

Embedded documents lưu trữ dữ liệu liên quan trong một cấu trúc document duy nhất. Một document có thể chứa các mảng và sub-documents với dữ liệu liên quan. Các mô hình dữ liệu phi chuẩn hóa này cho phép ứng dụng truy xuất dữ liệu liên quan trong một thao tác cơ sở dữ liệu duy nhất.

*Mô hình dữ liệu với các trường nhúng chứa tất cả thông tin liên quan.*

Đối với nhiều trường hợp sử dụng trong MongoDB, mô hình dữ liệu phi chuẩn hóa là tối ưu.

Để tìm hiểu về điểm mạnh và điểm yếu của việc nhúng documents, xem phần "Embedded Data Models".

### Tham chiếu (References)

References lưu trữ mối quan hệ giữa dữ liệu bằng cách bao gồm các liên kết, gọi là tham chiếu, từ document này đến document khác. Ví dụ, trường `customerId` trong collection `orders` chỉ ra tham chiếu đến một document trong collection `customers`.

Ứng dụng có thể giải quyết các tham chiếu này để truy cập dữ liệu liên quan. Nhìn chung, đây là các mô hình dữ liệu chuẩn hóa.

*Mô hình dữ liệu sử dụng tham chiếu để liên kết documents. Cả document `contact` và document `access` đều chứa tham chiếu đến document `user`.*

Để tìm hiểu về điểm mạnh và điểm yếu của việc sử dụng tham chiếu, xem phần "References".

## Các cân nhắc bổ sung về mô hình dữ liệu

Các yếu tố sau có thể ảnh hưởng đến cách bạn lên kế hoạch mô hình dữ liệu.

### Dữ liệu trùng lặp và tính nhất quán

Khi bạn nhúng dữ liệu liên quan trong một document duy nhất, bạn có thể sao chép dữ liệu giữa hai collections. Việc sao chép dữ liệu cho phép ứng dụng truy vấn thông tin liên quan về nhiều thực thể trong một truy vấn duy nhất trong khi tách biệt các thực thể một cách hợp lý trong mô hình của bạn.

Ví dụ, collection `products` lưu trữ năm đánh giá gần đây nhất trong document sản phẩm. Những đánh giá đó cũng được lưu trữ trong collection `reviews`, chứa tất cả các đánh giá sản phẩm. Khi một đánh giá mới được viết, các thao tác ghi sau đây xảy ra:

1. Đánh giá được chèn vào collection `reviews`.
2. Mảng đánh giá gần đây trong collection `products` được cập nhật với `$pop` và `$push`.

Nếu dữ liệu trùng lặp không được cập nhật thường xuyên, thì có rất ít công việc bổ sung cần thiết để giữ cho hai collections nhất quán. Tuy nhiên, nếu dữ liệu trùng lặp được cập nhật thường xuyên, việc sử dụng tham chiếu để liên kết dữ liệu liên quan có thể là cách tiếp cận tốt hơn.

Trước khi bạn sao chép dữ liệu, hãy xem xét các yếu tố sau:

- Tần suất cập nhật dữ liệu trùng lặp.
- Lợi ích hiệu suất cho các thao tác đọc khi dữ liệu được sao chép.

Để tìm hiểu thêm, xem phần "Handle Duplicate Data".

### Indexing

Để cải thiện hiệu suất cho các truy vấn mà ứng dụng của bạn chạy thường xuyên, hãy tạo các indexes trên các trường thường được truy vấn. Khi ứng dụng phát triển, theo dõi việc sử dụng indexes để đảm bảo rằng indexes vẫn hỗ trợ các truy vấn liên quan.

### Ràng buộc phần cứng

Khi thiết kế schema, hãy xem xét phần cứng triển khai của bạn, đặc biệt là lượng RAM khả dụng. Documents lớn hơn sử dụng nhiều RAM hơn, có thể khiến ứng dụng đọc từ đĩa và làm giảm hiệu suất. Khi có thể, thiết kế schema sao cho chỉ các trường liên quan được trả về bởi các truy vấn. Phương pháp này đảm bảo rằng working set của ứng dụng không phát triển quá lớn một cách không cần thiết.

### Tính nguyên tử của Single Document

Trong MongoDB, một thao tác ghi là nguyên tử ở cấp độ của một document duy nhất, ngay cả khi thao tác sửa đổi nhiều embedded documents trong một document duy nhất. Điều này có nghĩa là nếu một thao tác cập nhật ảnh hưởng đến một số sub-documents, thì hoặc tất cả các sub-documents đó được cập nhật, hoặc thao tác hoàn toàn thất bại và không có cập nhật nào xảy ra.

Một mô hình dữ liệu phi chuẩn hóa với dữ liệu nhúng kết hợp tất cả dữ liệu liên quan trong một document duy nhất thay vì chuẩn hóa qua nhiều documents và collections. Mô hình dữ liệu này cho phép các thao tác nguyên tử, trái ngược với mô hình chuẩn hóa mà các thao tác ảnh hưởng đến nhiều documents.

Để biết thêm thông tin, xem phần "Atomicity".

# Các yếu tố hoạt động và mô hình dữ liệu trong MongoDB

Việc mô hình hóa dữ liệu ứng dụng cho MongoDB cần xem xét các yếu tố hoạt động khác nhau ảnh hưởng đến hiệu suất của MongoDB. Các mô hình dữ liệu khác nhau có thể:
- Cho phép truy vấn hiệu quả hơn
- Tăng thông lượng của các thao tác chèn và cập nhật
- Phân phối hoạt động đến cụm phân mảnh hiệu quả hơn

Khi phát triển mô hình dữ liệu, hãy phân tích tất cả các thao tác đọc và ghi của ứng dụng kết hợp với các cân nhắc sau.

## Tính nguyên tử (Atomicity)

Trong MongoDB:
- Thao tác ghi là nguyên tử ở cấp độ một tài liệu đơn lẻ, ngay cả khi thao tác sửa đổi nhiều tài liệu nhúng trong một tài liệu duy nhất
- Khi một thao tác ghi đơn lẻ sửa đổi nhiều tài liệu (ví dụ: `db.collection.updateMany()`), việc sửa đổi mỗi tài liệu là nguyên tử, nhưng thao tác nói chung thì không

### Mô hình dữ liệu nhúng

Mô hình dữ liệu nhúng kết hợp tất cả dữ liệu liên quan trong một tài liệu duy nhất thay vì chuẩn hóa trên nhiều tài liệu và bộ sưu tập. Mô hình dữ liệu này tạo điều kiện cho các thao tác nguyên tử.

### Giao dịch đa tài liệu

Đối với các mô hình dữ liệu lưu trữ tham chiếu giữa các phần dữ liệu liên quan, ứng dụng phải phát hành các thao tác đọc và ghi riêng biệt để truy xuất và sửa đổi các phần dữ liệu liên quan này.

Đối với các tình huống yêu cầu tính nguyên tử của việc đọc và ghi nhiều tài liệu (trong một hoặc nhiều bộ sưu tập), MongoDB hỗ trợ các giao dịch phân tán, bao gồm cả giao dịch trên các bộ nhân bản và các cụm phân mảnh.

> **Quan trọng**: Trong hầu hết các trường hợp, một giao dịch phân tán phát sinh chi phí hiệu suất lớn hơn so với việc ghi tài liệu đơn lẻ, và khả năng có sẵn của các giao dịch phân tán không nên là sự thay thế cho thiết kế lược đồ hiệu quả. Đối với nhiều tình huống, mô hình dữ liệu phi chuẩn hóa (tài liệu nhúng và mảng) sẽ tiếp tục là tối ưu cho dữ liệu và trường hợp sử dụng của bạn.

## Phân mảnh (Sharding)

MongoDB sử dụng phân mảnh để cung cấp khả năng mở rộng theo chiều ngang. Các cụm này hỗ trợ triển khai với các tập dữ liệu lớn và các thao tác thông lượng cao. Phân mảnh cho phép người dùng phân vùng một bộ sưu tập trong một cơ sở dữ liệu để phân phối các tài liệu của bộ sưu tập trên một số phiên bản mongod hoặc mảnh.

Để phân phối dữ liệu và lưu lượng ứng dụng trong một bộ sưu tập phân mảnh, MongoDB sử dụng khóa phân mảnh (shard key). Việc chọn khóa phân mảnh phù hợp có ý nghĩa quan trọng đối với hiệu suất, và có thể bật hoặc ngăn chặn cô lập truy vấn và tăng khả năng ghi.

## Chỉ mục (Indexes)

Sử dụng chỉ mục để cải thiện hiệu suất cho các truy vấn phổ biến. Xây dựng chỉ mục trên các trường xuất hiện thường xuyên trong các truy vấn và cho tất cả các thao tác trả về kết quả được sắp xếp. MongoDB tự động tạo một chỉ mục duy nhất trên trường `_id`.

Khi tạo chỉ mục, hãy xem xét các hành vi sau:

- Mỗi chỉ mục yêu cầu ít nhất 8 kB không gian dữ liệu
- Thêm một chỉ mục có một số tác động tiêu cực đến hiệu suất cho các thao tác ghi
- Đối với các bộ sưu tập có tỷ lệ ghi-đọc cao, chỉ mục là tốn kém vì mỗi lần chèn cũng phải cập nhật bất kỳ chỉ mục nào
- Các bộ sưu tập có tỷ lệ đọc-ghi cao thường được hưởng lợi từ các chỉ mục bổ sung
- Chỉ mục không ảnh hưởng đến các thao tác đọc không được lập chỉ mục
- Khi hoạt động, mỗi chỉ mục tiêu thụ không gian đĩa và bộ nhớ

## Số lượng lớn các bộ sưu tập

Trong một số tình huống, bạn có thể chọn lưu trữ thông tin liên quan trong một số bộ sưu tập thay vì trong một bộ sưu tập duy nhất.

Ví dụ về bộ sưu tập logs:

```javascript
{ log: "dev", ts: ..., info: ... }
{ log: "debug", ts: ..., info: ...}
```

Nếu tổng số tài liệu thấp, bạn có thể nhóm tài liệu vào bộ sưu tập theo loại, như `logs_dev` và `logs_debug`.

Khi sử dụng mô hình có số lượng lớn bộ sưu tập, hãy xem xét:

- Mỗi bộ sưu tập có một mức tối thiểu nhất định của chi phí vài kilobyte
- Mỗi chỉ mục, bao gồm cả chỉ mục trên `_id`, yêu cầu ít nhất 8 kB không gian dữ liệu
- Đối với mỗi cơ sở dữ liệu, một tệp không gian tên duy nhất (tức là `<database>.ns`) lưu trữ tất cả dữ liệu meta cho cơ sở dữ liệu đó

## Bộ sưu tập chứa số lượng lớn tài liệu nhỏ

Bạn nên xem xét nhúng vì lý do hiệu suất nếu bạn có một bộ sưu tập với số lượng lớn tài liệu nhỏ. Nếu bạn có thể nhóm các tài liệu nhỏ này theo một số mối quan hệ hợp lý và bạn thường xuyên truy xuất tài liệu theo nhóm này, bạn có thể xem xét "cuộn lên" (rolling-up) các tài liệu nhỏ thành tài liệu lớn hơn chứa một mảng các tài liệu nhúng.

Lợi ích:
- Truy vấn để truy xuất một nhóm tài liệu liên quan đến đọc tuần tự và ít truy cập đĩa ngẫu nhiên hơn
- Có ít bản sao hơn của các trường chung và ít mục nhập khóa liên quan hơn trong chỉ mục tương ứng

Tuy nhiên, nếu bạn thường chỉ cần truy xuất một tập con của tài liệu trong nhóm, thì "cuộn lên" có thể không cải thiện hiệu suất.

## Tối ưu hóa lưu trữ cho tài liệu nhỏ

Mỗi tài liệu MongoDB chứa một lượng chi phí nhất định. Chi phí này thường không đáng kể nhưng trở nên đáng kể nếu tất cả tài liệu chỉ có vài byte.

Các chiến lược tối ưu hóa:

### Sử dụng trường `_id` một cách rõ ràng

MongoDB tự động thêm trường `_id` vào mỗi tài liệu và tạo một ObjectId 12-byte duy nhất. Để tối ưu hóa việc sử dụng lưu trữ, người dùng có thể chỉ định một giá trị cho trường `_id` khi chèn tài liệu vào bộ sưu tập.

### Sử dụng tên trường ngắn hơn

Ví dụ, thay vì:
```javascript
{ last_name: "Smith", best_score: 3.9 }
```

Bạn có thể sử dụng:
```javascript
{ lname: "Smith", score: 3.9 }
```

Điều này có thể tiết kiệm 9 byte cho mỗi tài liệu.

> **Lưu ý**: Việc rút ngắn tên trường làm giảm tính biểu đạt và không mang lại lợi ích đáng kể cho các tài liệu lớn hơn. Tên trường ngắn hơn không làm giảm kích thước của chỉ mục.

### Nhúng tài liệu

Trong một số trường hợp, bạn có thể muốn nhúng tài liệu vào tài liệu khác để tiết kiệm chi phí cho mỗi tài liệu.

## Quản lý vòng đời dữ liệu

Các quyết định mô hình hóa dữ liệu nên xem xét việc quản lý vòng đời dữ liệu:

- Tính năng **Time to Live (TTL)** của bộ sưu tập giúp hết hạn tài liệu sau một khoảng thời gian
- **Bộ sưu tập giới hạn** (Capped Collections) cung cấp quản lý first-in-first-out (FIFO) của tài liệu đã chèn và hỗ trợ hiệu quả các thao tác chèn và đọc tài liệu dựa trên thứ tự chèn

---
# Connecting to a MongoDB Database

# Connection Strings

> Sử dụng menu thả xuống "Select your language" ở góc trên bên phải để cài đặt ngôn ngữ cho các ví dụ sau.

Bạn có thể sử dụng connection strings để định nghĩa kết nối giữa các instance MongoDB và các đích đến sau:

- Ứng dụng của bạn khi kết nối sử dụng drivers.
- Công cụ như MongoDB Compass và MongoDB Shell (mongosh).

## Tương thích

Bạn có thể sử dụng connection strings để kết nối đến các deployment được host trong các môi trường sau:

- **MongoDB Atlas**: Dịch vụ được quản lý hoàn toàn cho các deployment MongoDB trên cloud
- **MongoDB Enterprise**: Phiên bản MongoDB dựa trên đăng ký, tự quản lý
- **MongoDB Community**: Phiên bản MongoDB nguồn mở, miễn phí sử dụng và tự quản lý

Hoàn thành các bước sau để tìm connection string của bạn.

## Tìm MongoDB Atlas Connection String

### Atlas CLI

**Atlas UI**  
Để tìm MongoDB Atlas connection string bằng Atlas CLI, hãy cài đặt và kết nối từ Atlas CLI, sau đó chạy lệnh sau. Thay `<clusterName>` bằng tên của MongoDB Atlas cluster và thay `<projectId>` bằng project ID.

```
atlas clusters connectionStrings describe <clusterName> --projectId <projectId>
```

Để tìm hiểu thêm, xem `atlas clusters connectionStrings describe`.

MongoDB Atlas connection string của bạn sẽ giống như ví dụ sau:

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@cluster0.example.mongodb.net/?retryWrites=true&w=majority
```

## Tìm Connection String cho Self-Hosted Deployment

Nếu bạn đã kết nối với MongoDB Enterprise hoặc MongoDB Community deployment tự host, hãy chạy phương thức `db.getMongo()` để trả về connection string.

Nếu bạn không kết nối với deployment, bạn có thể xác định connection string dựa trên loại kết nối bạn muốn sử dụng. Xem **SRV Connection Format** để tìm hiểu cú pháp connection string SRV hoặc **Standard Connection String Format** để tìm hiểu cú pháp connection string tiêu chuẩn.

Connection string tự host của bạn sẽ giống các ví dụ sau:

### SRV Connection String

### Standard Connection String

### Replica Set

### Sharded Cluster

### Standalone

Connection string replica set sau bao gồm các thành phần:
- Tùy chọn `replicaSet`
- Hostname của (các) instance mongod như được liệt kê trong cấu hình replica set
- Nó xác thực với user `myDatabaseUser` với mật khẩu `D1fficultP%40ssw0rd` để thực thi kiểm soát truy cập

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com/?authSource=admin&replicaSet=myRepl
```

Nếu tên người dùng hoặc mật khẩu bao gồm các ký tự sau, những ký tự đó phải được chuyển đổi bằng percent encoding:

```
$ : / ? # [ ] @
```

Để biết danh sách đầy đủ các tùy chọn connection string, xem **SRV Connection Format** hoặc **Standard Connection String Format**. Để xem thêm ví dụ, xem **Connection String Examples**.

## Connection String Formats

Bạn có thể chỉ định MongoDB connection string bằng một trong các định dạng sau:

- **SRV Connection Format**: Connection string với hostname tương ứng với DNS SRV record. Driver hoặc mongosh của bạn truy vấn record để xác định máy chủ nào đang chạy các instance mongod hoặc mongos.
- **Standard Connection String Format**: Connection string chỉ định tất cả các máy chủ đang chạy các instance mongod hoặc mongos.

MongoDB Atlas clusters sử dụng SRV connection format trừ khi bạn kết nối đến online archive.

### SRV Connection Format

MongoDB hỗ trợ danh sách seed được xây dựng từ DNS. Sử dụng DNS để xây dựng danh sách máy chủ khả dụng cho phép triển khai linh hoạt hơn và khả năng thay đổi các máy chủ trong rotation mà không cần cấu hình lại clients.

URI connection scheme SRV có dạng sau:

```
mongodb+srv://[username:password@]host[/[defaultauthdb][?options]]
```

Để xem thêm ví dụ, xem **Connection String Examples**.

#### Connection String Components

Connection string bao gồm các thành phần sau:

| Thành phần | Mô tả |
|------------|-------|
| mongodb:// hoặc mongodb+srv:// | Tiền tố bắt buộc để xác định đây là chuỗi ở định dạng kết nối tiêu chuẩn (mongodb://) hoặc định dạng kết nối SRV (mongodb+srv://). Để tìm hiểu thêm về từng định dạng, xem **Standard Connection String Format** và **SRV Connection Format**. |
| username:password@ | Tùy chọn. Thông tin xác thực.<br><br>Nếu được chỉ định, client sẽ cố gắng xác thực người dùng với authSource. Nếu authSource không được chỉ định, client sẽ cố gắng xác thực người dùng với defaultauthdb. Và nếu defaultauthdb không được chỉ định, sẽ xác thực với database admin.<br><br>Nếu tên người dùng hoặc mật khẩu bao gồm các ký tự sau, những ký tự đó phải được chuyển đổi bằng percent encoding:<br><br>$ : / ? # [ ] @<br><br>Xem thêm authSource. |
| host[:port] | Máy chủ (và số cổng tùy chọn) nơi instance mongod (hoặc instance mongos cho sharded cluster) đang chạy. Bạn có thể chỉ định hostname, địa chỉ IP hoặc UNIX domain socket. Chỉ định càng nhiều máy chủ càng tốt cho topo triển khai của bạn:<br><br>- Đối với standalone, chỉ định hostname của instance mongod standalone.<br>- Đối với replica set, chỉ định hostname của (các) instance mongod như được liệt kê trong cấu hình replica set.<br>- Đối với sharded cluster, chỉ định hostname của (các) instance mongos.<br><br>Nếu số cổng không được chỉ định, cổng mặc định 27017 được sử dụng.<br><br>Nếu bạn sử dụng định dạng kết nối SRV URI, bạn chỉ có thể chỉ định một máy chủ và không có cổng. Nếu không, driver hoặc mongosh sẽ báo lỗi phân tích và không thực hiện phân giải DNS. |
| /defaultauthdb | Tùy chọn. Cơ sở dữ liệu xác thực sẽ sử dụng nếu connection string bao gồm thông tin xác thực username:password@ nhưng tùy chọn authSource không được chỉ định.<br><br>Nếu cả authSource và defaultauthdb đều không được chỉ định, client sẽ cố gắng xác thực người dùng đã chỉ định với cơ sở dữ liệu admin. |
| ?<options> | Tùy chọn. Chuỗi truy vấn chỉ định các tùy chọn kết nối cụ thể dưới dạng các cặp <name>=<value>. Xem **Connection String Options** để biết mô tả đầy đủ về các tùy chọn này.<br><br>Nếu connection string không chỉ định database/ bạn phải chỉ định dấu gạch chéo (/) giữa máy chủ cuối cùng và dấu hỏi (?) bắt đầu chuỗi các tùy chọn. |

Để tận dụng danh sách seed DNS, hãy sử dụng cú pháp tương tự như connection string tiêu chuẩn với tiền tố là `mongodb+srv` thay vì `mongodb` tiêu chuẩn. `+srv` chỉ định cho client rằng hostname theo sau tương ứng với DNS SRV record. Driver hoặc mongosh sau đó sẽ truy vấn DNS cho record để xác định máy chủ nào đang chạy các instance mongod hoặc mongos.

> **Lưu ý**: Việc sử dụng bổ ngữ connection string `+srv` tự động đặt tùy chọn tls (hoặc tùy chọn tương đương ssl) thành true cho kết nối. Bạn có thể ghi đè hành vi này bằng cách đặt rõ ràng tùy chọn tls (hoặc tùy chọn tương đương ssl) thành false với tls=false (hoặc ssl=false) trong chuỗi truy vấn.

Khi sử dụng định dạng `+srv`, bạn phải chỉ định hostname, domain và top-level domain (TLD) theo định dạng sau: `<hostname>.<domain>.<TLD>`. Bảng này cho thấy các placeholder tương ứng với các giá trị ví dụ:

| Placeholder | Ví dụ |
|-------------|-------|
| <hostname> | server |
| <domain> | example |
| <TLD> | com |
| <hostname>.<domain>.<TLD> | server.example.com |

Ví dụ này hiển thị connection string danh sách seed DNS sử dụng đúng định dạng `<hostname>.<domain>.<TLD>`. Nó xác thực là người dùng myDatabaseUser với mật khẩu D1fficultP%40ssw0rd:

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@server.example.com/
```

Cấu hình DNS tương ứng giống như:

```
Record                            TTL   Class    Priority Weight Port  Target
_mongodb._tcp.server.example.com. 86400 IN SRV   0        5      27317 mongodb1.example.com.
_mongodb._tcp.server.example.com. 86400 IN SRV   0        5      27017 mongodb2.example.com.
```

Các bản ghi SRV riêng lẻ phải có định dạng `_mongodb._tcp.<hostname>.<domain>.<TLD>`.

Khi client kết nối với một thành viên của danh sách seed, client sẽ truy xuất danh sách các thành viên replica set mà nó có thể kết nối. Clients thường sử dụng DNS aliases trong danh sách seed của họ, điều này có nghĩa là máy chủ có thể trả về danh sách server khác với danh sách seed ban đầu. Nếu điều này xảy ra, clients sẽ sử dụng hostnames được cung cấp bởi replica set thay vì hostnames được liệt kê trong danh sách seed để đảm bảo rằng các thành viên replica set có thể được truy cập thông qua hostnames trong cấu hình replica set kết quả.

> **Quan trọng**: Các hostnames được trả về trong bản ghi SRV phải có cùng parent domain (trong ví dụ này là example.com) với hostname đã cho. Nếu parent domains và hostname không khớp, bạn sẽ không thể kết nối.

Ví dụ này hiển thị connection string danh sách seed DNS thiếu `<hostname>`. Điều này không chính xác và gây ra lỗi.

```
# Connection string này thiếu <hostname> và gây ra lỗi kết nối
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@example.com/
```

Giống như connection string tiêu chuẩn, connection string danh sách seed DNS hỗ trợ chỉ định các tùy chọn dưới dạng chuỗi truy vấn. Với connection string danh sách seed DNS, bạn cũng có thể chỉ định các tùy chọn sau thông qua TXT record:

- replicaSet
- authSource

Bạn chỉ có thể chỉ định một TXT record cho mỗi instance mongod. Nếu nhiều TXT records xuất hiện trong DNS và/hoặc nếu TXT record chứa tùy chọn khác ngoài replicaSet hoặc authSource, client sẽ trả về lỗi.

TXT record cho mục DNS server.example.com sẽ giống như:

```
Record              TTL   Class    Text
server.example.com. 86400 IN TXT   "replicaSet=mySet&authSource=authDB"
```

Kết hợp lại, các bản ghi DNS SRV và các tùy chọn được chỉ định trong TXT record sẽ giải quyết thành connection string định dạng tiêu chuẩn sau:

```
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb1.example.com:27317,mongodb2.example.com:27017/?replicaSet=mySet&authSource=authDB
```

Bạn có thể ghi đè các tùy chọn được chỉ định trong TXT record bằng cách truyền tùy chọn trong chuỗi truy vấn. Trong ví dụ sau, chuỗi truy vấn đã cung cấp một override cho tùy chọn authSource được cấu hình trong TXT record của mục DNS ở trên.

```
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@server.example.com/?connectTimeoutMS=300000&authSource=aDifferentAuthDB
```

Với override cho authSource, connection string tương đương ở định dạng tiêu chuẩn sẽ là:

```
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb1.example.com:27317,mongodb2.example.com:27017/?connectTimeoutMS=300000&replicaSet=mySet&authSource=aDifferentAuthDB
```

> **Lưu ý**: Tùy chọn mongodb+srv sẽ thất bại nếu không có DNS khả dụng với các bản ghi tương ứng với hostname được xác định trong connection string. Nếu bạn sử dụng bổ ngữ connection string +srv, tùy chọn tls (hoặc tùy chọn tương đương ssl) sẽ được đặt thành true cho kết nối. Bạn có thể ghi đè hành vi này bằng cách đặt rõ ràng tùy chọn tls (hoặc tùy chọn tương đương ssl) thành false với tls=false (hoặc ssl=false) trong chuỗi truy vấn.

Để biết ví dụ về việc kết nối mongosh với replica set bằng định dạng kết nối danh sách seed DNS, xem **mongosh Connection Options**.

### Standard Connection String Format

Phần này mô tả định dạng tiêu chuẩn của MongoDB connection URI được sử dụng để kết nối với MongoDB standalone deployment, replica set hoặc sharded cluster tự host.

Schema kết nối URI tiêu chuẩn có dạng:

```
mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
```

Để xem thêm ví dụ, xem **Connection String Examples**.

#### Connection String Database Options

Bạn có thể chỉ định cơ sở dữ liệu mặc định trong trường [/defaultauthdb] của connection string. Client sử dụng cơ sở dữ liệu [/defaultauthdb] được chỉ định làm cơ sở dữ liệu mặc định. Nếu không được chỉ định bởi connection string, cơ sở dữ liệu mặc định là cơ sở dữ liệu test.

Bạn có thể chỉ định cơ sở dữ liệu xác thực trong connection string của bạn bằng tùy chọn kết nối authSource. Nếu được chỉ định, client sử dụng cơ sở dữ liệu này để xác minh danh tính và thông tin đăng nhập của bạn. Nếu authSource không được chỉ định, nó mặc định là cơ sở dữ liệu [/defaultauthdb]. Nếu cả authSource và [/defaultauthdb] đều không được chỉ định, authSource mặc định là cơ sở dữ liệu admin.

Connection string sau đặt cơ sở dữ liệu mặc định thành myDefaultDB và cơ sở dữ liệu xác thực thành admin:

```
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017/myDefaultDB?authSource=admin
```

#### Connection String Components

Connection string bao gồm các thành phần sau:

| Thành phần | Mô tả |
|------------|-------|
| mongodb:// hoặc mongodb+srv:// | Tiền tố bắt buộc để xác định đây là chuỗi ở định dạng kết nối tiêu chuẩn (mongodb://) hoặc định dạng kết nối SRV (mongodb+srv://). Để tìm hiểu thêm về từng định dạng, xem **Standard Connection String Format** và **SRV Connection Format**. |
| username:password@ | Tùy chọn. Thông tin xác thực.<br><br>Nếu được chỉ định, client sẽ cố gắng xác thực người dùng với authSource. Nếu authSource không được chỉ định, client sẽ cố gắng xác thực người dùng với defaultauthdb. Và nếu defaultauthdb không được chỉ định, sẽ xác thực với database admin.<br><br>Nếu tên người dùng hoặc mật khẩu bao gồm các ký tự sau, những ký tự đó phải được chuyển đổi bằng percent encoding:<br><br>$ : / ? # [ ] @<br><br>Xem thêm authSource. |
| host[:port] | Máy chủ (và số cổng tùy chọn) nơi instance mongod (hoặc instance mongos cho sharded cluster) đang chạy. Bạn có thể chỉ định hostname, địa chỉ IP hoặc UNIX domain socket. Chỉ định càng nhiều máy chủ càng tốt cho topo triển khai của bạn:<br><br>- Đối với standalone, chỉ định hostname của instance mongod standalone.<br>- Đối với replica set, chỉ định hostname của (các) instance mongod như được liệt kê trong cấu hình replica set.<br>- Đối với sharded cluster, chỉ định hostname của (các) instance mongos.<br><br>Nếu số cổng không được chỉ định, cổng mặc định 27017 được sử dụng.<br><br>Nếu bạn sử dụng định dạng kết nối SRV URI, bạn chỉ có thể chỉ định một máy chủ và không có cổng. Nếu không, driver hoặc mongosh sẽ báo lỗi phân tích và không thực hiện phân giải DNS. |
| /defaultauthdb | Tùy chọn. Cơ sở dữ liệu xác thực sẽ sử dụng nếu connection string bao gồm thông tin xác thực username:password@ nhưng tùy chọn authSource không được chỉ định.<br><br>Nếu cả authSource và defaultauthdb đều không được chỉ định, client sẽ cố gắng xác thực người dùng đã chỉ định với cơ sở dữ liệu admin. |
| ?<options> | Tùy chọn. Chuỗi truy vấn chỉ định các tùy chọn kết nối cụ thể dưới dạng các cặp <name>=<value>. Xem **Connection String Options** để biết mô tả đầy đủ về các tùy chọn này.<br><br>Nếu connection string không chỉ định database/ bạn phải chỉ định dấu gạch chéo (/) giữa máy chủ cuối cùng và dấu hỏi (?) bắt đầu chuỗi các tùy chọn. |

---
# Connecting to MongoDB in Python

```bash
pip install 'pymongo[srv]'
```

###  Insert

### Finding documents
```bash
use <database>
```

```bash
db.<collection>.find()
```

#### There are many ways to find document
- { field: { `$eq`:  < value > } }
- {field: < value > }
```bash
db.zips.find({ state: "AZ"})
```

- `$in` operator
```
db.<collection>.find({
	<field> : { $in:
		[<value>, <value>, ...]
	}
})
```

### Comparision operators
# MongoDB Query Operators

| Name | Description |
| --- | --- |
| `$eq` | Matches values that are equal to a specified value. |
| `$gt` | Matches values that are greater than a specified value. |
| `$gte` | Matches values that are greater than or equal to a specified value. |
| `$in` | Matches any of the values specified in an array. |
| $lt` | Matches values that are less than a specified value. |
| `$lte` | Matches values that are less than or equal to a specified value. |
| `$ne` | Matches all values that are not equal to a specified value. |
| `$nin` | Matches none of the values specified in an array. |


```bash
<field> : { <operator> : <value> }
```

 ### Query on arraay elements

 `$eleMatch`

 ```bash
db.account.find({
	products: {
		$eleMatch: {$eq: "InvestmentStock"}
		}
	})
```

**Use the $elemMatch operator to find all documents that contain the specified subdocument. For example:**


```
db.sales.find({
  items: {
    $elemMatch: { name: "laptop", price: { $gt: 800 }, quantity: { $gte: 1 } },
  },
})
```

### Logical operators
- `$and`
- `$or`

Use implicit $and to select documents that match multiple expressions. For example:
```bash
db.routes.find({ "airline.name": "Southwest Airlines", stops: { $gte: 1 } })
```

Use the $or operator to select documents that match at least one of the included expressions. For example:

```bash
db.routes.find({
  $or: [{ dst_airport: "SEA" }, { src_airport: "SEA" }],
})
```

Use the $and operator to use multiple $or expressions in your query.

```bash
db.routes.find({
  $and: [
    { $or: [{ dst_airport: "SEA" }, { src_airport: "SEA" }] },
    { $or: [{ "airline.name": "American Airlines" }, { airplane: 320 }] },
  ]
})
```

### Replacing a Document in MongoDB
Replacing a Document in MongoDB
To replace documents in MongoDB, we use the `replaceOne()` method. The `replaceOne()` method takes the following parameters:
* `filter`: A query that matches the document to replace.
* `replacement`: The new document to replace the old one with.
* `options`: An object that specifies options for the update.
In the previous video, we use the `_id` field to filter the document. In our replacement document, we provide the entire document that should be inserted in its place. Here's the example code from the video:

```bash
db.books.replaceOne(
  {
    _id: ObjectId("6282afeb441a74a98dbbec4e"),
  },
  {
    title: "Data Science Fundamentals for Python and MongoDB",
    isbn: "1484235967",
    publishedDate: new Date("2018-5-10"),
    thumbnailUrl:
      "https://m.media-amazon.com/images/I/71opmUBc2wL._AC_UY218_.jpg",
    authors: ["David Paper"],
    categories: ["Data Science"],
  }
)
```

### Updating MongoDB Documents by Using `updateOne()`
The `updateOne()` method accepts a filter document, an update document, and an optional options object. MongoDB provides update operators and options to help you update documents. In this section, we'll cover three of them: `$set`, `upsert`, and `$push`.
`$set`
The `$set` operator replaces the value of a field with the specified value, as shown in the following code:

```bash
db.podcasts.updateOne(
  {
    _id: ObjectId("5e8f8f8f8f8f8f8f8f8f8f8"),
  },

  {
    $set: {
      subscribers: 98562,
    },
  }
)
```

`upsert`
The `upsert` option creates a new document if no documents match the filtered criteria. Here's an example:

```bash
db.podcasts.updateOne(
  { title: "The Developer Hub" },
  { $set: { topics: ["databases", "MongoDB"] } },
  { upsert: true }
)
```

`$push`
The `$push` operator adds a new value to the `hosts` array field. Here's an example:

```bash
db.podcasts.updateOne(
  { _id: ObjectId("5e8f8f8f8f8f8f8f8f8f8f8") },
  { $push: { hosts: "Nic Raboy" } }
)
```

### Updating MongoDB Documents by Using `findAndModify()`
The `findAndModify()` method is used to find and replace a single document in MongoDB. It accepts a filter document, a replacement document, and an optional options object. The following code shows an example:

```bash
db.podcasts.findAndModify({
  query: { _id: ObjectId("6261a92dfee1ff300dc80bf1") },
  update: { $inc: { subscribers: 1 } },
  new: true,
})
```

### Updating MongoDB Documents by Using `updateMany()`
To update multiple documents, use the `updateMany()` method. This method accepts a filter document, an update document, and an optional options object. The following code shows an example:

```
db.books.updateMany(
  { publishedDate: { $lt: new Date("2019-01-01") } },
  { $set: { status: "LEGACY" } }
)
```


### Deleting Documents in MongoDB
To delete documents, use the deleteOne() or deleteMany() methods. Both methods accept a filter document and an options object.

#### Delete One Document
The following code shows an example of the deleteOne() method:
```bash
db.podcasts.deleteOne({ _id: Objectid("6282c9862acb966e76bbf20a") })
```
#### Delete Many Documents
The following code shows an example of the deleteMany() method:
```bash
db.podcasts.deleteMany({category: “crime”})
```

## MongoDB Operations Summary

### ✅ Document Updates and Modifications

- **Replaced a document**  
  Sử dụng `db.collection.replaceOne()` để thay thế toàn bộ một document.

- **Updated a specific field**  
  Sử dụng toán tử `$set` trong `db.collection.updateOne()` để cập nhật giá trị của một trường cụ thể.

- **Added a value to an array**  
  Sử dụng toán tử `$push` trong `db.collection.updateOne()` để thêm một giá trị mới vào mảng trong document.

- **Upsert operation**  
  Sử dụng tùy chọn `upsert` trong `db.collection.updateOne()` để thêm mới document nếu chưa tồn tại, hoặc cập nhật nếu đã tồn tại.

- **Find and modify a document**  
  Sử dụng `db.collection.findAndModify()` để tìm và đồng thời sửa đổi một document.

- **Update multiple documents**  
  Sử dụng `db.collection.updateMany()` để cập nhật nhiều document cùng lúc.

### ❌ Document Deletion

- **Delete a document**  
  Sử dụng `db.collection.deleteOne()` để xóa một document khỏi collection.


## Sắp xếp và Giới hạn Kết quả Truy vấn trong MongoDB

### Sắp xếp Kết quả (Sorting Results)

Để sắp xếp kết quả truy vấn theo một thứ tự nhất định, sử dụng phương thức `cursor.sort()`. Trong dấu ngoặc của `sort()`, truyền vào một object chỉ định các trường (field) cần sắp xếp và thứ tự sắp xếp. Sử dụng giá trị `1` để sắp xếp **tăng dần** (ascending) và `-1` để sắp xếp **giảm dần** (descending).

#### Cú pháp:
```javascript
db.collection.find(<query>).sort(<sort>)
```

#### Ví dụ:
```javascript
// Lấy dữ liệu tất cả công ty thuộc lĩnh vực âm nhạc, sắp xếp theo tên từ A đến Z.
db.companies.find({ category_code: "music" }).sort({ name: 1 });
```

Để đảm bảo kết quả trả về có thứ tự nhất quán, nên bao gồm một trường chứa giá trị duy nhất (unique) trong `sort`. Một cách đơn giản là thêm trường `_id` vào `sort`.

#### Ví dụ:
```javascript
// Lấy dữ liệu tất cả công ty âm nhạc, sắp xếp theo tên từ A đến Z, đảm bảo thứ tự nhất quán.
db.companies.find({ category_code: "music" }).sort({ name: 1, _id: 1 });
```

### Giới hạn Kết quả (Limiting Results)

Để giới hạn số lượng tài liệu (document) được trả về, sử dụng phương thức `cursor.limit()`. Trong dấu ngoặc của `limit()`, chỉ định số lượng tài liệu tối đa cần trả về.

#### Cú pháp:
```javascript
db.companies.find(<query>).limit(<number>)
```

#### Ví dụ:
```javascript
// Lấy 3 công ty âm nhạc có số lượng nhân viên cao nhất, đảm bảo thứ tự nhất quán.
db.companies
  .find({ category_code: "music" })
  .sort({ number_of_employees: -1, _id: 1 })
  .limit(3);
```

## Trả về Dữ liệu Cụ thể từ Truy vấn trong MongoDB

### Thêm Projection Document

Để chỉ định các trường (field) muốn bao gồm hoặc loại trừ trong tập hợp kết quả, thêm một **projection document** làm tham số thứ hai trong lệnh `db.collection.find()`.

#### Cú pháp:
```javascript
db.collection.find(<query>, <projection>)
```

### Bao gồm một Trường (Include a Field)

Để bao gồm một trường cụ thể trong kết quả, đặt giá trị của trường đó là `1` trong **projection document**.

#### Cú pháp:
```javascript
db.collection.find(<query>, { <field>: 1 })
```

#### Ví dụ:
```javascript
// Trả về tất cả các cuộc kiểm tra nhà hàng - chỉ lấy trường business_name, result và _id
db.inspections.find(
  { sector: "Restaurant - 818" },
  { business_name: 1, result: 1 }
)
```

### Loại trừ một Trường (Exclude a Field)

Để loại trừ một trường khỏi kết quả, đặt giá trị của trường đó là `0` trong **projection document**.

#### Cú pháp:
```javascript
db.collection.find(<query>, { <field>: 0, <field>: 0 })
```

#### Ví dụ:
```javascript
// Trả về tất cả các cuộc kiểm tra có kết quả "Pass" hoặc "Warning" - loại trừ trường date và zip code
db.inspections.find(
  { result: { $in: ["Pass", "Warning"] } },
  { date: 0, "address.zip": 0 }
)
```

#### Lưu ý:
- Trường `_id` được bao gồm mặc định trong kết quả. Tuy nhiên, bạn có thể loại bỏ nó bằng cách đặt giá trị của `_id` là `0` trong **projection document**.

#### Ví dụ:
```javascript
// Trả về tất cả các cuộc kiểm tra nhà hàng - chỉ lấy trường business_name và result, loại bỏ _id
db.inspections.find(
  { sector: "Restaurant - 818" },
  { business_name: 1, result: 1, _id: 0 }
)
```

## Đếm Số Lượng Tài Liệu trong Một Collection của MongoDB

### Đếm Tài Liệu (Count Documents)

Để đếm số lượng tài liệu (document) khớp với một truy vấn, sử dụng phương thức `db.collection.countDocuments()`. Phương thức này nhận hai tham số: một **query document** và một **options document**.

#### Cú pháp:
```javascript
db.collection.countDocuments(<query>, <options>)
```

- **query**: Chỉ định các tài liệu cần được đếm.

#### Ví dụ:
```javascript
// Đếm tổng số tài liệu trong collection trips
db.trips.countDocuments({})
```

```javascript
// Đếm số chuyến đi kéo dài trên 120 phút của người dùng loại "Subscriber"
db.trips.countDocuments({ tripduration: { $gt: 120 }, usertype: "Subscriber" })
```

# Giới thiệu về Aggregation trong MongoDB

Phần này bao gồm các định nghĩa quan trọng và ví dụ về một **aggregation pipeline** trong MongoDB.

## Định nghĩa

- **Aggregation**: Quá trình thu thập và tóm tắt dữ liệu.
- **Stage**: Một phương thức tích hợp sẵn được thực hiện trên dữ liệu, nhưng không thay đổi dữ liệu vĩnh viễn.
- **Aggregation pipeline**: Một chuỗi các **stage** được thực hiện trên dữ liệu theo thứ tự.

## Cấu trúc của Aggregation Pipeline

```javascript
db.collection.aggregate([
    {
        $stage1: {
            { expression1 },
            { expression2 }...
        }
    },
    {
        $stage2: {
            { expression1 }...
        }
    }
])
```

## Sử dụng $match và $group trong Aggregation Pipeline

### $match

**$match** lọc các tài liệu (document) dựa trên các điều kiện được chỉ định.

```javascript
{
    $match: {
        "field_name": "value"
    }
}
```

### $group

**$group** nhóm các tài liệu theo một **group key**.

```javascript
{
    $group: {
        _id: <expression>, // Group key
        <field>: { <accumulator>: <expression> }
    }
}
```

### Ví dụ $match và $group

Pipeline dưới đây tìm các tài liệu có trường `state` là `"CA"`, sau đó nhóm các tài liệu theo `city` và đếm tổng số mã zip trong bang California.

```javascript
db.zips.aggregate([
    {
        $match: {
            state: "CA"
        }
    },
    {
        $group: {
            _id: "$city",
            totalZips: { $count: {} }
        }
    }
])
```

## Sử dụng $sort và $limit trong Aggregation Pipeline

### $sort

**$sort** sắp xếp tất cả tài liệu đầu vào và trả về theo thứ tự đã sắp xếp. Sử dụng `1` cho thứ tự **tăng dần** và `-1` cho thứ tự **giảm dần**.

```javascript
{
    $sort: {
        "field_name": 1
    }
}
```

### $limit

**$limit** giới hạn số lượng tài liệu trả về.

```javascript
{
    $limit: 5
}
```

### Ví dụ $sort và $limit

Pipeline dưới đây sắp xếp các tài liệu theo trường `pop` theo thứ tự giảm dần (giá trị lớn nhất trước) và giới hạn kết quả chỉ trả về 5 tài liệu đầu tiên.

```javascript
db.zips.aggregate([
    {
        $sort: {
            pop: -1
        }
    },
    {
        $limit: 5
    }
])
```

## Sử dụng $project, $count và $set trong Aggregation Pipeline

### $project

**$project** chỉ định các trường sẽ xuất hiện trong tài liệu đầu ra. Giá trị `1` để bao gồm trường, `0` để loại bỏ trường. Trường cũng có thể được gán giá trị mới.

```javascript
{
    $project: {
        state: 1,
        zip: 1,
        population: "$pop",
        _id: 0
    }
}
```

### $set

**$set** tạo các trường mới hoặc thay đổi giá trị của các trường hiện có, sau đó trả về tài liệu với các trường mới.

```javascript
{
    $set: {
        place: {
            $concat: ["$city", ",", "$state"]
        },
        pop: 10000
    }
}
```

### $count

**$count** tạo một tài liệu mới, chứa số lượng tài liệu tại thời điểm đó trong pipeline, gán vào tên trường được chỉ định.

```javascript
{
    $count: "total_zips"
}
```

## $out trong Aggregation

### Định nghĩa

**$out** ghi các tài liệu được trả về bởi pipeline vào một collection được chỉ định. Bạn có thể chỉ định cả database đầu ra.

- **$out** phải là **stage cuối cùng** trong pipeline.
- **$out** cho phép aggregation framework trả về tập hợp kết quả với bất kỳ kích thước nào.

### Cảnh báo

Nếu collection được chỉ định bởi **$out** đã tồn tại, **$out** sẽ thay thế hoàn toàn collection hiện tại bằng collection kết quả mới sau khi aggregation hoàn tất.

### Cú pháp

- Chỉ định collection đầu ra (trong cùng database):

```javascript
{ $out: "<output-collection>" }
```

- Chỉ định cả database và collection đầu ra:

```javascript
{ $out: { db: "<output-db>", coll: "<output-collection>" } }
```

- Từ MongoDB 7.0.3 và 7.1, hỗ trợ ghi vào time series collection:

```javascript
{
    $out: {
        db: "<output-db>",
        coll: "<output-collection>",
        timeseries: {
            timeField: "<field-name>",
            metaField: "<field-name>",
            granularity: "seconds" || "minutes" || "hours"
        }
    }
}
```

### Lưu ý quan trọng

- **Thay đổi Granularity của Time Series**: Sau khi tạo time series collection, bạn có thể sửa đổi **granularity** bằng phương thức `collMod`. Tuy nhiên, bạn chỉ có thể tăng khoảng thời gian bao phủ bởi mỗi bucket, không thể giảm nó.

# Làm việc với Index trong MongoDB

## Tạo Index trên Một Trường (Single Field Index)

Sử dụng `createIndex()` để tạo một index mới trong một collection. Trong dấu ngoặc của `createIndex()`, truyền vào một object chứa trường (field) và thứ tự sắp xếp.

```javascript
db.customers.createIndex({
    birthdate: 1
})
```

### Tạo Index Độc nhất trên Một Trường (Unique Single Field Index)

Thêm `{ unique: true }` làm tham số thứ hai (tùy chọn) trong `createIndex()` để đảm bảo giá trị của trường index là duy nhất. Sau khi index độc nhất được tạo, mọi thao tác chèn hoặc cập nhật có giá trị trùng lặp trong trường index sẽ thất bại.

```javascript
db.customers.createIndex({
    email: 1
}, {
    unique: true
})
```

**Lưu ý**: MongoDB chỉ tạo index độc nhất nếu không có giá trị trùng lặp trong các trường được chọn làm index.

### Xem Các Index trong Collection

Sử dụng `getIndexes()` để xem tất cả các index đã được tạo trong một collection.

```javascript
db.customers.getIndexes()
```

### Kiểm tra Index được Sử dụng trong Truy vấn

Sử dụng `explain()` khi thực hiện một truy vấn để xem **Execution Plan**. Kế hoạch này cung cấp chi tiết về các giai đoạn thực thi (IXSCAN, COLLSCAN, FETCH, SORT, v.v.):

- **IXSCAN**: Truy vấn sử dụng một index và hiển thị index được chọn.
- **COLLSCAN**: Thực hiện quét toàn bộ collection, không sử dụng index.
- **FETCH**: Đọc tài liệu từ collection.
- **SORT**: Sắp xếp tài liệu trong bộ nhớ.

```javascript
db.customers.explain().find({
    birthdate: {
        $gt: ISODate("1995-08-01")
    }
})
```

```javascript
db.customers.explain().find({
    birthdate: {
        $gt: ISODate("1995-08-01")
    }
}).sort({
    email: 1
})
```

## Hiểu về Multikey Index

Nếu một index trên một trường đơn hoặc index ghép (compound) bao gồm một trường dạng mảng (array), thì index đó là **multikey index**.

### Tạo Multikey Index trên Một Trường

Sử dụng `createIndex()` để tạo index trên một trường mảng. Trong ví dụ này, `accounts` là một trường mảng.

```javascript
db.customers.createIndex({
    accounts: 1
})
```

### Xem Các Index trong Collection

Sử dụng `getIndexes()` để xem tất cả các index đã được tạo.

```javascript
db.customers.getIndexes()
```

### Kiểm tra Index được Sử dụng trong Truy vấn

Sử dụng `explain()` để kiểm tra **Execution Plan** của truy vấn:

```javascript
db.customers.explain().find({
    accounts: 627788
})
```

## Làm việc với Compound Index

### Tạo Compound Index

Sử dụng `createIndex()` để tạo index trên hai hoặc nhiều trường. Trong dấu ngoặc của `createIndex()`, truyền vào một object chứa các trường và thứ tự sắp xếp.

```javascript
db.customers.createIndex({
    active: 1,
    birthdate: -1,
    name: 1
})
```

### Thứ tự các Trường trong Compound Index

Thứ tự các trường và thứ tự sắp xếp rất quan trọng. Nên liệt kê các trường theo thứ tự sau: **Equality**, **Sort**, và **Range**.

- **Equality**: Trường khớp với một giá trị duy nhất trong truy vấn.
- **Sort**: Trường được dùng để sắp xếp kết quả.
- **Range**: Trường được lọc trong một khoảng giá trị hợp lệ.

Ví dụ truy vấn sau bao gồm một phép khớp **equality** trên trường `active`, sắp xếp theo `birthdate` (giảm dần) và `name` (tăng dần), đồng thời lọc khoảng trên `birthdate`:

```javascript
db.customers.find({
    birthdate: {
        $gte: ISODate("1977-01-01")
    },
    active: true
}).sort({
    birthdate: -1,
    name: 1
})
```

Index hiệu quả cho truy vấn này:

```javascript
db.customers.createIndex({
    active: 1,
    birthdate: -1,
    name: 1
})
```

### Xem Các Index trong Collection

Sử dụng `getIndexes()` để xem tất cả các index.

```javascript
db.customers.getIndexes()
```

### Kiểm tra Index được Sử dụng trong Truy vấn

Sử dụng `explain()` để xem **Execution Plan**:

```javascript
db.customers.explain().find({
    birthdate: {
        $gte: ISODate("1977-01-01")
    },
    active: true
}).sort({
    birthdate: -1,
    name: 1
})
```

### Phủ toàn bộ Truy vấn bằng Index (Cover a Query)

Một index **phủ** (cover) một truy vấn khi MongoDB không cần lấy dữ liệu từ bộ nhớ vì tất cả dữ liệu cần thiết đã được index trả về.

Sử dụng **projection** để chỉ trả về các trường cần thiết, đảm bảo các trường này nằm trong index. Ví dụ, thêm projection `{ name: 1, birthdate: 1, _id: 0 }` để giới hạn kết quả chỉ chứa `name` và `birthdate`:

```javascript
db.customers.explain().find({
    birthdate: {
        $gte: ISODate("1977-01-01")
    },
    active: true
}, {
    name: 1,
    birthdate: 1,
    _id: 0
}).sort({
    birthdate: -1,
    name: 1
})
```

**Execution Plan** sẽ hiển thị:

- **IXSCAN**: Quét index ghép.
- **PROJECTION_COVERED**: Tất cả thông tin cần thiết được trả về bởi index, không cần lấy từ bộ nhớ.

## Xóa Index

### Xem Các Index trong Collection

Sử dụng `getIndexes()` để xem tất cả các index. Mọi collection luôn có một index mặc định trên trường `_id`, được MongoDB sử dụng nội bộ và không thể xóa.

```javascript
db.customers.getIndexes()
```

### Xóa Một Index

Sử dụng `dropIndex()` để xóa một index hiện có. Trong dấu ngoặc của `dropIndex()`, truyền vào một object đại diện cho khóa index hoặc cung cấp tên index dưới dạng chuỗi.

Xóa index theo tên:

```javascript
db.customers.dropIndex("active_1_birthdate_-1_name_1")
```

Xóa index theo khóa:

```javascript
db.customers.dropIndex({
    active: 1,
    birthdate: -1,
    name: 1
})
```

### Xóa Nhiều Index

Sử dụng `dropIndexes()` để xóa tất cả các index trong collection, ngoại trừ index mặc định trên `_id`.

```javascript
db.customers.dropIndexes()
```

`dropIndexes()` cũng có thể nhận một mảng tên index để xóa một danh sách index cụ thể:

```javascript
db.collection.dropIndexes([
    "index1name",
    "index2name",
    "index3name"
])
```

# Sử dụng $search và Facets trong MongoDB Atlas Search

## Sử dụng $search với Compound Operators

Toán tử **compound** trong giai đoạn `$search` cho phép cân nhắc mức độ quan trọng của các trường khác nhau và lọc kết quả mà không cần tạo thêm các giai đoạn aggregation. Có bốn tùy chọn cho toán tử **compound**: `must`, `mustNot`, `should`, và `filter`.

- **`must`**: Loại trừ các bản ghi không đáp ứng tiêu chí.
- **`mustNot`**: Loại trừ các bản ghi đáp ứng tiêu chí.
- **`should`**: Cho phép ưu tiên các bản ghi đáp ứng tiêu chí để xuất hiện đầu tiên.
- **`filter`**: Loại bỏ các bản ghi không đáp ứng tiêu chí.

### Ví dụ về $search với Compound Operators

```javascript
{
    $search: {
        "compound": {
            "must": [{
                "text": {
                    "query": "field",
                    "path": "habitat"
                }
            }],
            "should": [{
                "range": {
                    "gte": 45,
                    "path": "wingspan_cm",
                    "score": { "constant": { "value": 5 } }
                }
            }]
        }
    }
}
```

## Nhóm Kết quả Tìm kiếm bằng Facets

### $searchMeta và facet

**$searchMeta** là một giai đoạn aggregation trong Atlas Search, hiển thị siêu dữ liệu (metadata) liên quan đến tìm kiếm. Khi kết quả tìm kiếm được chia thành các nhóm (buckets) bằng **facet**, thông tin về các nhóm này sẽ được hiển thị trong giai đoạn `$searchMeta`, vì chúng phản ánh cách kết quả tìm kiếm được định dạng.

### Ví dụ về $searchMeta với facet

```javascript
{
    $searchMeta: {
        "facet": {
            "operator": {
                "text": {
                    "query": ["Northern Cardinal"],
                    "path": "common_name"
                }
            },
            "facets": {
                "sightingWeekFacet": {
                    "type": "date",
                    "path": "sighting",
                    "boundaries": [
                        ISODate("2022-01-01"),
                        ISODate("2022-01-08"),
                        ISODate("2022-01-15"),
                        ISODate("2022-01-22")
                    ],
                    "default": "other"
                }
            }
        }
    }
}
```

### Giải thích

- **`facet`**: Toán tử trong `$searchMeta`, xác định cách chia kết quả thành các nhóm (buckets).
- **`operator`**: Chỉ định truy vấn tìm kiếm (search query).
- **`facets`**: Định nghĩa các nhóm (buckets) cho facet, ví dụ như nhóm theo ngày trong trường `sighting`.

# ACID Transactions trong MongoDB

## Điểm chính
- **ACID** là viết tắt của Atomicity, Consistency, Isolation, và Durability, đảm bảo các giao dịch cơ sở dữ liệu được xử lý đáng tin cậy.
- MongoDB hỗ trợ các giao dịch ACID, đặc biệt là giao dịch đa tài liệu từ phiên bản 4.0, phù hợp cho các ứng dụng cần tính toàn vẹn dữ liệu.
- Giao dịch trong MongoDB có thể hoạt động trên nhiều tài liệu, bộ sưu tập, và thậm chí cả các cụm phân tán, nhưng cần được sử dụng cẩn thận để tránh ảnh hưởng đến hiệu suất.
- Các phương pháp như nhúng dữ liệu hoặc sử dụng trigger có thể là lựa chọn thay thế trong một số trường hợp để giảm chi phí hiệu suất.

### Tổng quan
ACID transactions là một tập hợp các thuộc tính giúp đảm bảo rằng các thao tác cơ sở dữ liệu, như chuyển tiền hoặc cập nhật kho, được thực hiện một cách an toàn và đáng tin cậy. Trong MongoDB, một cơ sở dữ liệu NoSQL, các giao dịch này cho phép bạn thực hiện nhiều thao tác trên các tài liệu khác nhau mà vẫn đảm bảo dữ liệu không bị hỏng hoặc không nhất quán.

### Cách MongoDB xử lý
MongoDB, từ phiên bản 4.0, đã giới thiệu hỗ trợ cho các giao dịch đa tài liệu, nghĩa là bạn có thể thực hiện các thao tác trên nhiều tài liệu và bộ sưu tập trong một giao dịch duy nhất. Ví dụ, khi chuyển tiền từ tài khoản này sang tài khoản khác, cả hai thao tác (trừ tiền và cộng tiền) sẽ được thực hiện cùng nhau hoặc không thực hiện gì cả.

### Khi nào nên sử dụng
Giao dịch ACID trong MongoDB rất hữu ích cho các ứng dụng như ngân hàng, thương mại điện tử, hoặc quản lý kho, nơi dữ liệu cần được cập nhật đồng thời ở nhiều nơi. Tuy nhiên, vì chúng có thể làm chậm hiệu suất, bạn nên cân nhắc sử dụng các phương pháp khác, như nhúng dữ liệu vào một tài liệu duy nhất, nếu có thể.

---

# Báo cáo chi tiết về ACID Transactions trong MongoDB

## Giới thiệu
ACID là viết tắt của **Atomicity** (Tính nguyên tử), **Consistency** (Tính nhất quán), **Isolation** (Tính cô lập), và **Durability** (Tính bền vững). Những thuộc tính này đảm bảo rằng các giao dịch cơ sở dữ liệu được xử lý một cách đáng tin cậy, ngay cả khi xảy ra lỗi hoặc sự cố hệ thống. MongoDB, một cơ sở dữ liệu NoSQL định hướng tài liệu, hỗ trợ các giao dịch ACID, đặc biệt là các giao dịch đa tài liệu từ phiên bản 4.0, giúp các nhà phát triển xây dựng các ứng dụng yêu cầu tính toàn vẹn dữ liệu cao.

## Các thuộc tính ACID trong MongoDB

### Atomicity (Tính nguyên tử)
- **Định nghĩa**: Đảm bảo rằng tất cả các thao tác trong một giao dịch được coi là một đơn vị duy nhất, hoặc tất cả thành công hoặc tất cả thất bại.
- **Trong MongoDB**: 
  - Các thao tác ghi trên một tài liệu duy nhất luôn có tính nguyên tử.
  - Đối với giao dịch đa tài liệu, MongoDB đảm bảo rằng tất cả các thay đổi được thực hiện hoặc bị hủy bỏ cùng nhau, duy trì tính toàn vẹn dữ liệu trên nhiều tài liệu, bộ sưu tập, bộ sao chép (replica sets), và cụm phân tán (sharded clusters).
  - Ví dụ: Khi chuyển 1000 đồng từ tài khoản A sang tài khoản B, cả hai thao tác (trừ tiền từ A và cộng tiền vào B) sẽ được thực hiện hoặc không thực hiện gì cả.

### Consistency (Tính nhất quán)
- **Định nghĩa**: Đảm bảo rằng một giao dịch đưa cơ sở dữ liệu từ một trạng thái hợp lệ sang một trạng thái hợp lệ khác, tuân thủ các quy tắc và ràng buộc đã định nghĩa.
- **Trong MongoDB**: 
  - MongoDB cung cấp sự linh hoạt trong mô hình dữ liệu, cho phép nhà phát triển lựa chọn giữa việc chuẩn hóa dữ liệu trên nhiều bộ sưu tập hoặc nhúng dữ liệu liên quan vào một tài liệu duy nhất.
  - Trong các giao dịch đa tài liệu, tính nhất quán được duy trì bằng cách đảm bảo rằng tất cả các thao tác trong giao dịch tuân thủ các quy tắc và ràng buộc của ứng dụng.
  - Ví dụ: Nếu một giao dịch cập nhật số dư tài khoản và lịch sử giao dịch, MongoDB đảm bảo rằng cả hai đều được cập nhật chính xác hoặc không thay đổi gì.

### Isolation (Tính cô lập)
- **Định nghĩa**: Đảm bảo rằng các giao dịch đồng thời không can thiệp lẫn nhau, ngăn chặn việc một giao dịch nhìn thấy trạng thái trung gian của giao dịch khác.
- **Trong MongoDB**: 
  - MongoDB sử dụng **snapshot isolation** cho các giao dịch, nghĩa là mỗi giao dịch hoạt động trên một bản chụp (snapshot) của dữ liệu tại thời điểm bắt đầu giao dịch, không thấy các thay đổi từ các giao dịch khác đang chạy đồng thời.
  - Điều này giúp tránh các vấn đề như đọc bẩn (dirty reads) hoặc đọc không lặp lại (non-repeatable reads).
  - Ví dụ: Nếu hai giao dịch cùng cố gắng cập nhật số dư tài khoản, chúng sẽ không xung đột vì mỗi giao dịch hoạt động trên một bản chụp riêng.

### Durability (Tính bền vững)
- **Định nghĩa**: Đảm bảo rằng một khi giao dịch được xác nhận (committed), nó sẽ được lưu trữ vĩnh viễn, ngay cả khi xảy ra sự cố hệ thống.
- **Trong MongoDB**: 
  - MongoDB đạt được tính bền vững thông qua cơ chế ghi trước (write-ahead logging), cụ thể là **Operation Log (OpLog)**.
  - Tất cả các thao tác ghi được ghi vào OpLog, được đồng bộ hóa với đĩa định kỳ (mặc định mỗi 60 giây), đảm bảo rằng các giao dịch đã xác nhận sẽ tồn tại sau sự cố.
  - Ví dụ: Sau khi một giao dịch chuyển tiền được xác nhận, dữ liệu sẽ được lưu trữ an toàn, ngay cả khi máy chủ bị mất điện.

## Các phương pháp xử lý tính nhất quán trong MongoDB
MongoDB cung cấp nhiều phương pháp để xử lý tính nhất quán, mỗi phương pháp có ưu và nhược điểm riêng:

| **Phương pháp** | **Mô tả** | **Ảnh hưởng hiệu suất** | **Trường hợp sử dụng** |
|------------------|-----------|-------------------------|-----------------------|
| [Transactions](https://www.mongodb.com/docs/manual/core/transactions/) | Cập nhật nhiều bộ sưu tập trong một thao tác nguyên tử duy nhất. | Có thể cao do tranh chấp đọc (read contention). | Khi ứng dụng cần trả về dữ liệu cập nhật ngay lập tức và có thể chấp nhận ảnh hưởng hiệu suất trong trường hợp đọc nặng. |
| [Embedding Related Data](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/) | Lưu trữ dữ liệu liên quan trong một tài liệu duy nhất. | Thấp đến trung bình, tùy thuộc vào kích thước tài liệu và index. | Khi dữ liệu liên quan luôn được đọc/cập nhật cùng nhau, đơn giản hóa thiết kế schema và tránh thao tác `$lookup`. |
| [Atlas Database Triggers](https://www.mongodb.com/docs/atlas/app-services/triggers/database-triggers/) | Tự động cập nhật một bộ sưu tập khi bộ sưu tập khác được cập nhật. | Thấp đến trung bình, có thể có độ trễ. | Khi ứng dụng có thể chấp nhận dữ liệu hơi cũ và người dùng có thể thấy dữ liệu chưa cập nhật trong thời gian ngắn. |

## Cách sử dụng giao dịch trong MongoDB
Để thực hiện một giao dịch trong MongoDB, bạn cần sử dụng một phiên (session) và các phương thức giao dịch. Dưới đây là quy trình cơ bản:

1. **Bắt đầu phiên**: Sử dụng `startSession()` để tạo một phiên.
2. **Bắt đầu giao dịch**: Gọi `startTransaction()` trong phiên.
3. **Thực hiện thao tác**: Thực hiện các thao tác đọc và ghi trong phiên giao dịch.
4. **Xác nhận hoặc hủy**: Sử dụng `commitTransaction()` để xác nhận hoặc `abortTransaction()` để hủy giao dịch.

Ví dụ mã JavaScript (sử dụng MongoDB Node.js driver):

```javascript
const { MongoClient } = require("mongodb");

async function run() {
    const client = new MongoClient("mongodb://localhost:27017");
    try {
        await client.connect();
        const db = client.db("bank");
        const session = client.startSession();
        try {
            await session.withTransaction(async () => {
                const accounts = db.collection("accounts");
                await accounts.updateOne(
                    { account_id: "A" },
                    { $inc: { balance: -1000 } },
                    { session }
                );
                await accounts.updateOne(
                    { account_id: "B" },
                    { $inc: { balance: 1000 } },
                    { session }
                );
            });
            console.log("Giao dịch thành công!");
        } finally {
            await session.endSession();
        }
    } finally {
        await client.close();
    }
}
run().catch(console.dir);
```

## Các thực hành tốt nhất khi sử dụng giao dịch
- **Chia nhỏ giao dịch dài**: Tránh các giao dịch kéo dài bằng cách chia thành các giao dịch nhỏ hơn để tránh hết thời gian chờ (mặc định 60 giây, có thể mở rộng).
- **Giới hạn số lượng tài liệu**: Giới hạn giao dịch ở mức 1.000 tài liệu được sửa đổi để duy trì hiệu suất.
- **Sử dụng read/write concern phù hợp**: Từ MongoDB 5.0, write concern mặc định là "majority", đảm bảo tính nhất quán cao.
- **Xử lý lỗi và thử lại**: Thêm cơ chế xử lý lỗi và thử lại cho các lỗi tạm thời (transient errors).
- **Cân nhắc hiệu suất**: Giao dịch trên nhiều phân mảnh (shards) có thể tốn kém, vì vậy hãy sử dụng cẩn thận.

## Các trường hợp sử dụng giao dịch đa tài liệu
- **Ứng dụng ngân hàng**: Đảm bảo chuyển tiền nguyên tử giữa các tài khoản ([Banking Example](https://github.com/mongodb-developer/nodejs-quickstart/blob/master/transaction-bankingexample.js)).
- **Xử lý thanh toán**: Quản lý các giao dịch liên quan đến nhiều bước hoặc bộ sưu tập.
- **Nền tảng giao dịch**: Duy trì tính nhất quán cho các giao dịch phức tạp trên nhiều bản ghi.
- **Hệ thống chuỗi cung ứng và đặt chỗ**: Chuyển giao quyền sở hữu hoặc cập nhật kho trên các bộ sưu tập khác nhau.
- **Hệ thống thanh toán**: Đồng bộ hóa các bản ghi chi tiết và tóm tắt.

## Hạn chế và cân nhắc
- **Hiệu suất**: Giao dịch đa tài liệu có thể làm giảm hiệu suất, đặc biệt trong các cụm phân tán hoặc khi có tranh chấp đọc/ghi cao.
- **Mô hình dữ liệu**: Mô hình tài liệu của MongoDB khuyến khích nhúng dữ liệu liên quan vào một tài liệu duy nhất, điều này có thể giảm nhu cầu sử dụng giao dịch trong nhiều trường hợp.
- **Thay thế**: Trong một số trường hợp, nhúng dữ liệu hoặc sử dụng Atlas Database Triggers có thể là lựa chọn hiệu quả hơn về hiệu suất so với giao dịch.

## Kết luận
Hỗ trợ giao dịch ACID của MongoDB cung cấp cho các nhà phát triển công cụ để đảm bảo tính toàn vẹn dữ liệu trong các thao tác phức tạp, đa tài liệu. Bằng cách hiểu và áp dụng các nguyên tắc của Atomicity, Consistency, Isolation, và Durability, cùng với các thực hành tốt nhất và phương pháp được cung cấp bởi MongoDB, các nhà phát triển có thể xây dựng các ứng dụng mạnh mẽ và đáng tin cậy. Tuy nhiên, cần cân nhắc cẩn thận giữa tính toàn vẹn dữ liệu và hiệu suất khi sử dụng giao dịch, đặc biệt trong các hệ thống quy mô lớn.

## Key Citations
- [MongoDB ACID Transactions Overview](https://www.mongodb.com/resources/basics/databases/acid-transactions)
- [MongoDB Official Transactions Documentation](https://www.mongodb.com/docs/manual/core/transactions/)
- [MongoDB Multi-Document ACID Transactions](https://www.mongodb.com/products/capabilities/transactions)
- [MongoDB Data Modeling: Embedding vs References](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)
- [Atlas Database Triggers Documentation](https://www.mongodb.com/docs/atlas/app-services/triggers/database-triggers/)
- [Node.js Transaction Banking Example](https://github.com/mongodb-developer/nodejs-quickstart/blob/master/transaction-bankingexample.js)


# Giao dịch Đa Tài Liệu trong MongoDB

- Giao dịch đa tài liệu đảm bảo tính toàn vẹn dữ liệu khi cập nhật nhiều tài liệu.
- Thường được sử dụng trong các ứng dụng như ngân hàng hoặc kinh doanh.
- Có thể thực hiện hoặc hủy giao dịch để duy trì trạng thái cơ sở dữ liệu.
- Yêu cầu MongoDB phiên bản 4.0 trở lên với replica set hoặc sharded cluster.

## Sử dụng Giao dịch

Để thực hiện một giao dịch đa tài liệu trong MongoDB, bạn cần tạo một phiên (session), bắt đầu giao dịch, thực hiện các thao tác cơ sở dữ liệu, và sau đó xác nhận (commit) giao dịch. Các bước này đảm bảo rằng tất cả các thao tác được thực hiện như một đơn vị nguyên tử, nghĩa là hoặc tất cả thành công hoặc không có thay đổi nào được áp dụng.

**Các bước thực hiện**:

1. **Bắt đầu phiên (session)**: Tạo một phiên để quản lý giao dịch.
2. **Bắt đầu giao dịch**: Khởi động giao dịch trong phiên.
3. **Lấy collection**: Xác định cơ sở dữ liệu và collection để thực hiện thao tác.
4. **Thực hiện thao tác**: Thêm các thao tác như cập nhật hoặc chèn tài liệu.
5. **Xác nhận giao dịch**: Lưu tất cả các thay đổi bằng cách xác nhận giao dịch.

**Ví dụ mã**:

```javascript
const session = db.getMongo().startSession()
session.startTransaction()
const account = session.getDatabase('bank').getCollection('accounts')
account.updateOne(
    { account_id: "A" },
    { $inc: { balance: -100 } },
    { session }
)
account.updateOne(
    { account_id: "B" },
    { $inc: { balance: 100 } },
    { session }
)
session.commitTransaction()
session.endSession()
```

Trong ví dụ này, giao dịch chuyển 100 đơn vị từ tài khoản A sang tài khoản B. Nếu cả hai thao tác thành công, giao dịch được xác nhận; nếu không, không có thay đổi nào được lưu.

## Hủy Giao dịch

Nếu bạn cần hoàn tác các thay đổi trước khi giao dịch hoàn tất, bạn có thể hủy (abort) giao dịch. Điều này sẽ khôi phục cơ sở dữ liệu về trạng thái ban đầu trước khi giao dịch bắt đầu, đảm bảo không có thay đổi nào được áp dụng.

**Các bước hủy**:

1. **Bắt đầu phiên và giao dịch**: Tương tự như khi sử dụng giao dịch.
2. **Thực hiện thao tác**: Thêm các thao tác cơ sở dữ liệu.
3. **Hủy giao dịch**: Sử dụng `abortTransaction()` để hủy các thay đổi.

**Ví dụ mã**:

```javascript
const session = db.getMongo().startSession()
session.startTransaction()
const account = session.getDatabase('bank').getCollection('accounts')
account.updateOne(
    { account_id: "A" },
    { $inc: { balance: -100 } },
    { session }
)
// Giả sử có lỗi xảy ra
session.abortTransaction()
session.endSession()
```

Trong trường hợp này, nếu có lỗi hoặc bạn quyết định không tiếp tục, `abortTransaction()` đảm bảo rằng số dư tài khoản A không bị thay đổi.

---

# Báo cáo chi tiết về Giao dịch Đa Tài Liệu trong MongoDB

## Tổng quan

Giao dịch đa tài liệu trong MongoDB cho phép thực hiện nhiều thao tác trên các tài liệu, bộ sưu tập, hoặc thậm chí các phân mảnh (shards) khác nhau như một đơn vị nguyên tử duy nhất. Điều này đảm bảo rằng hoặc tất cả các thao tác thành công, hoặc không có thay đổi nào được áp dụng, duy trì tính toàn vẹn dữ liệu. Được giới thiệu từ phiên bản 4.0, tính năng này rất quan trọng cho các ứng dụng như ngân hàng, thương mại điện tử, hoặc quản lý kho, nơi các cập nhật một phần có thể dẫn đến trạng thái không nhất quán.

Giao dịch đa tài liệu tuân thủ các thuộc tính **ACID**:

- **Atomicity** (Tính nguyên tử): Tất cả các thao tác trong giao dịch được thực hiện như một đơn vị duy nhất.
- **Consistency** (Tính nhất quán): Giao dịch đưa cơ sở dữ liệu từ trạng thái hợp lệ này sang trạng thái hợp lệ khác.
- **Isolation** (Tính cô lập): Các giao dịch được cô lập, không thấy trạng thái trung gian của nhau.
- **Durability** (Tính bền vững): Các thay đổi được xác nhận sẽ được lưu vĩnh viễn, ngay cả khi hệ thống gặp sự cố.

## Khi nào nên sử dụng

Giao dịch đa tài liệu thường được sử dụng trong các ứng dụng yêu cầu trao đổi giá trị giữa các bên, chẳng hạn như:

- **Ngân hàng**: Chuyển tiền giữa các tài khoản.
- **Thương mại điện tử**: Cập nhật đơn hàng và kho hàng đồng thời.
- **Quản lý kho**: Điều chỉnh số lượng tồn kho trên nhiều bản ghi.

Tuy nhiên, do giao dịch có thể ảnh hưởng đến hiệu suất, bạn nên cân nhắc nhúng dữ liệu liên quan vào một tài liệu duy nhất nếu có thể, vì các thao tác trên một tài liệu luôn có tính nguyên tử trong MongoDB.

## Sử dụng Giao dịch

Để thực hiện một giao dịch đa tài liệu, bạn cần sử dụng một phiên (session) để quản lý các thao tác. Dưới đây là các bước chi tiết:

1. **Tạo phiên**:
   ```javascript
   const session = db.getMongo().startSession()
   ```
   Phiên là một cơ chế để nhóm các thao tác giao dịch lại với nhau.

2. **Bắt đầu giao dịch**:
   ```javascript
   session.startTransaction()
   ```
   Điều này khởi động giao dịch, đảm bảo rằng tất cả các thao tác tiếp theo được thực hiện như một đơn vị nguyên tử.

3. **Lấy collection**:
   ```javascript
   const account = session.getDatabase('bank').getCollection('accounts')
   ```
   Xác định cơ sở dữ liệu và collection mà bạn muốn thao tác.

4. **Thực hiện thao tác**:
   Các thao tác như `insertOne`, `updateOne`, hoặc `deleteOne` có thể được thực hiện. Đảm bảo bao gồm tham số `{ session }` để liên kết thao tác với giao dịch.
   ```javascript
   account.updateOne(
       { account_id: "A" },
       { $inc: { balance: -100 } },
       { session }
   )
   account.updateOne(
       { account_id: "B" },
       { $inc: { balance: 100 } },
       { session }
   )
   ```

5. **Xác nhận giao dịch**:
   ```javascript
   session.commitTransaction()
   ```
   Nếu tất cả các thao tác thành công, `commitTransaction()` lưu các thay đổi vào cơ sở dữ liệu.

6. **Kết thúc phiên**:
   ```javascript
   session.endSession()
   ```
   Luôn gọi `endSession()` để giải phóng tài nguyên, bất kể giao dịch thành công hay thất bại.

**Ví dụ đầy đủ**:

```javascript
const session = db.getMongo().startSession()
try {
    session.startTransaction()
    const account = session.getDatabase('bank').getCollection('accounts')
    account.updateOne(
        { account_id: "A" },
        { $inc: { balance: -100 } },
        { session }
    )
    account.updateOne(
        { account_id: "B" },
        { $inc: { balance: 100 } },
        { session }
    )
    session.commitTransaction()
    console.log("Giao dịch thành công!")
} catch (error) {
    console.log("Lỗi giao dịch:", error)
    session.abortTransaction()
} finally {
    session.endSession()
}
```

Trong ví dụ này, giao dịch chuyển 100 đơn vị từ tài khoản A sang tài khoản B. Nếu cả hai thao tác cập nhật thành công, giao dịch được xác nhận. Nếu có lỗi, giao dịch sẽ bị hủy.

## Hủy Giao dịch

Nếu bạn cần hoàn tác các thay đổi trong giao dịch, bạn có thể gọi `abortTransaction()`. Điều này sẽ khôi phục cơ sở dữ liệu về trạng thái trước khi giao dịch bắt đầu.

**Các bước chi tiết**:

1. **Tạo phiên và bắt đầu giao dịch**:
   ```javascript
   const session = db.getMongo().startSession()
   session.startTransaction()
   ```

2. **Thực hiện thao tác**:
   ```javascript
   const account = session.getDatabase('bank').getCollection('accounts')
   account.updateOne(
       { account_id: "A" },
       { $inc: { balance: -100 } },
       { session }
   )
   ```

3. **Hủy giao dịch**:
   ```javascript
   session.abortTransaction()
   ```
   Nếu bạn quyết định không tiếp tục (ví dụ, do lỗi hoặc điều kiện không thỏa mãn), `abortTransaction()` đảm bảo rằng không có thay đổi nào được lưu.

4. **Kết thúc phiên**:
   ```javascript
   session.endSession()
   ```

**Ví dụ đầy đủ**:

```javascript
const session = db.getMongo().startSession()
try {
    session.startTransaction()
    const account = session.getDatabase('bank').getCollection('accounts')
    account.updateOne(
        { account_id: "A" },
        { $inc: { balance: -100 } },
        { session }
    )
    // Giả sử có lỗi hoặc điều kiện không thỏa mãn
    throw new Error("Không đủ số dư")
} catch (error) {
    console.log("Hủy giao dịch do:", error)
    session.abortTransaction()
} finally {
    session.endSession()
}
```

Trong ví dụ này, nếu tài khoản A không đủ số dư, giao dịch sẽ bị hủy, và số dư của tài khoản không thay đổi.

## Các thực hành tốt nhất

Để sử dụng giao dịch đa tài liệu hiệu quả, hãy tuân theo các thực hành sau:

- **Giữ giao dịch ngắn gọn**: Hạn chế số lượng thao tác trong một giao dịch để giảm thời gian khóa và cải thiện hiệu suất. MongoDB giới hạn giao dịch ở mức 1.000 tài liệu được sửa đổi để duy trì hiệu suất.
- **Xử lý lỗi**: Luôn bao gồm cơ chế xử lý lỗi để hủy giao dịch nếu cần. Sử dụng `try-catch` để bắt các lỗi và gọi `abortTransaction()` khi thích hợp.
- **Kết thúc phiên**: Đảm bảo gọi `session.endSession()` trong khối `finally` để giải phóng tài nguyên, ngay cả khi giao dịch thất bại.
- **Sử dụng read/write concern phù hợp**: Từ MongoDB 5.0, write concern mặc định là "majority", đảm bảo tính nhất quán cao. Bạn có thể điều chỉnh tùy thuộc vào yêu cầu ứng dụng.
- **Cân nhắc hiệu suất**: Giao dịch trên các cụm phân tán (sharded clusters) có thể tốn kém hơn. Nếu có thể, nhúng dữ liệu liên quan vào một tài liệu duy nhất để tránh sử dụng giao dịch.
- **Thử lại giao dịch**: Trong trường hợp lỗi tạm thời (transient errors), thêm logic thử lại giao dịch để tăng độ tin cậy.

## Hạn chế

Giao dịch đa tài liệu trong MongoDB có một số hạn chế cần lưu ý:

- **Yêu cầu triển khai**: Giao dịch chỉ được hỗ trợ trên replica sets hoặc sharded clusters, không áp dụng cho các phiên bản độc lập.
- **Hiệu suất**: Giao dịch có thể làm giảm hiệu suất, đặc biệt khi liên quan đến nhiều tài liệu hoặc phân mảnh.
- **Thời gian chờ**: Giao dịch có thời gian chờ mặc định là 60 giây, có thể được mở rộng nhưng cần được quản lý cẩn thận.
- **Thao tác không được hỗ trợ**: Một số thao tác, như thao tác trên capped collections hoặc một số lệnh quản trị, không thể được sử dụng trong giao dịch.

## Các trường hợp sử dụng

Giao dịch đa tài liệu rất hữu ích trong các tình huống sau:

| **Trường hợp sử dụng** | **Mô tả** | **Ví dụ** |
|-------------------------|-----------|-----------|
| Ngân hàng | Chuyển tiền giữa các tài khoản, đảm bảo số dư được cập nhật đồng thời. | Chuyển 100 đơn vị từ tài khoản A sang tài khoản B. |
| Thương mại điện tử | Cập nhật đơn hàng và kho hàng trong một giao dịch. | Xử lý đơn hàng và giảm số lượng tồn kho. |
| Quản lý kho | Điều chỉnh số lượng tồn kho trên nhiều bản ghi. | Cập nhật kho khi chuyển hàng giữa các kho. |
| Hệ thống thanh toán | Đồng bộ hóa chi tiết giao dịch và tóm tắt tài khoản. | Ghi lại giao dịch và cập nhật số dư tài khoản. |

## Kết luận

Giao dịch đa tài liệu trong MongoDB cung cấp một công cụ mạnh mẽ để đảm bảo tính toàn vẹn dữ liệu trong các thao tác phức tạp, đặc biệt trong các ứng dụng yêu cầu trao đổi giá trị như ngân hàng hoặc kinh doanh. Bằng cách sử dụng các phiên, bạn có thể thực hiện nhiều thao tác như một đơn vị nguyên tử, với tùy chọn xác nhận hoặc hủy giao dịch tùy thuộc vào kết quả. Tuy nhiên, để tối ưu hóa hiệu suất, hãy sử dụng giao dịch một cách có chọn lọc và cân nhắc các phương pháp thay thế như nhúng dữ liệu khi phù hợp. Với các thực hành tốt nhất và xử lý lỗi cẩn thận, bạn có thể xây dựng các ứng dụng đáng tin cậy và hiệu quả với MongoDB.

## Key Citations

- [MongoDB Transactions Documentation](https://www.mongodb.com/docs/manual/core/transactions/)
- [MongoDB Multi-Document ACID Transactions](https://www.mongodb.com/docs/manual/core/transactions/)
- [How To Use Transactions in MongoDB | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-transactions-in-mongodb)
- [An Overview of Multi-Document ACID Transactions in MongoDB | Severalnines](https://severalnines.com/blog/overview-multi-document-acid-transactions-mongodb-and-how-use-them/)



# Thao tác với MongoDB trong Python bằng PyMongo

Phần này hướng dẫn cách thực hiện các thao tác cơ bản như chèn, truy vấn, cập nhật, xóa tài liệu và tạo giao dịch đa tài liệu trong MongoDB bằng thư viện **PyMongo**.

## Chèn Tài Liệu (Inserting Documents)

### Chèn Một Tài Liệu (Insert One Document)

Để chèn một tài liệu vào collection, sử dụng phương thức `insert_one()` trên đối tượng collection. Phương thức này nhận một tài liệu làm tham số và trả về kết quả, bao gồm `_id` của tài liệu được chèn.

```python
from pymongo import MongoClient
import datetime

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Tạo tài liệu mới
new_account = {
    "account_holder": "Linus Torvalds",
    "account_id": "MDB829001337",
    "account_type": "checking",
    "balance": 50352434,
    "last_updated": datetime.datetime.utcnow(),
}

# Chèn tài liệu vào collection
result = accounts_collection.insert_one(new_account)

# In _id của tài liệu vừa chèn
document_id = result.inserted_id
print(f"_id của tài liệu vừa chèn: {document_id}")

# Đóng kết nối
client.close()
```

### Chèn Nhiều Tài Liệu (Insert Multiple Documents)

Để chèn nhiều tài liệu, sử dụng phương thức `insert_many()`. Phương thức này nhận một danh sách các tài liệu và trả về danh sách `_id` của các tài liệu được chèn.

```python
from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Tạo danh sách các tài liệu mới
new_accounts = [
    {
        "account_id": "MDB011235813",
        "account_holder": "Ada Lovelace",
        "account_type": "checking",
        "balance": 60218,
    },
    {
        "account_id": "MDB829000001",
        "account_holder": "Muhammad ibn Musa al-Khwarizmi",
        "account_type": "savings",
        "balance": 267914296,
    },
]

# Chèn các tài liệu vào collection
result = accounts_collection.insert_many(new_accounts)

# In số lượng và _id của các tài liệu vừa chèn
document_ids = result.inserted_ids
print("# tài liệu được chèn: " + str(len(document_ids)))
print(f"_id của các tài liệu: {document_ids}")

# Đóng kết nối
client.close()
```

## Truy vấn Tài Liệu (Querying Documents)

### Truy vấn Một Tài Liệu (Query for a Single Document)

Để lấy một tài liệu khớp với truy vấn, sử dụng phương thức `find_one()`. Phương thức này nhận một bộ lọc (filter) và trả về tài liệu đầu tiên khớp hoặc `None` nếu không tìm thấy.

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Bộ lọc truy vấn theo ObjectId
document_to_find = {"_id": ObjectId("62d6e04ecab6d8e1304974ae")}

# Thực hiện truy vấn
result = accounts_collection.find_one(document_to_find)

# In kết quả
pprint(result)

# Đóng kết nối
client.close()
```

### Truy vấn Nhiều Tài Liệu (Query for Multiple Documents)

Để lấy tất cả các tài liệu khớp với truy vấn, sử dụng phương thức `find()`. Phương thức này trả về một **Cursor**, cho phép duyệt qua các tài liệu khớp.

```python
from pymongo import MongoClient
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Bộ lọc truy vấn
documents_to_find = {"balance": {"$gt": 4700}}

# Thực hiện truy vấn
cursor = accounts_collection.find(documents_to_find)

# Duyệt và in các tài liệu
num_docs = 0
for document in cursor:
    num_docs += 1
    pprint(document)
    print()
print("# tài liệu tìm thấy: " + str(num_docs))

# Đóng kết nối
client.close()
```

## Cập nhật Tài Liệu (Updating Documents)

### Cập nhật Một Tài Liệu (Update a Single Document)

Để cập nhật một tài liệu, sử dụng phương thức `update_one()`. Phương thức này nhận hai tham số: một bộ lọc để xác định tài liệu và một tài liệu cập nhật xác định các thay đổi.

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Bộ lọc
document_to_update = {"_id": ObjectId("62d6e04ecab6d8e130497482")}

# Cập nhật
add_to_balance = {"$inc": {"balance": 100}}

# In tài liệu trước khi cập nhật
pprint(accounts_collection.find_one(document_to_update))

# Thực hiện cập nhật
result = accounts_collection.update_one(document_to_update, add_to_balance)
print("Tài liệu được cập nhật: " + str(result.modified_count))

# In tài liệu sau khi cập nhật
pprint(accounts_collection.find_one(document_to_update))

# Đóng kết nối
client.close()
```

### Cập nhật Nhiều Tài Liệu (Update Multiple Documents)

Để cập nhật nhiều tài liệu, sử dụng phương thức `update_many()`. Phương thức này cũng nhận bộ lọc và tài liệu cập nhật, áp dụng thay đổi cho tất cả các tài liệu khớp.

```python
from pymongo import MongoClient
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Bộ lọc
select_accounts = {"account_type": "savings"}

# Cập nhật
set_field = {"$set": {"minimum_balance": 100}}

# Thực hiện cập nhật
result = accounts_collection.update_many(select_accounts, set_field)

# In kết quả
print("Tài liệu khớp: " + str(result.matched_count))
print("Tài liệu được cập nhật: " + str(result.modified_count))
pprint(accounts_collection.find_one(select_accounts))

# Đóng kết nối
client.close()
```

## Xóa Tài Liệu (Deleting Documents)

### Xóa Một Tài Liệu (Delete a Single Document)

Để xóa một tài liệu, sử dụng phương thức `delete_one()`. Phương thức này nhận một bộ lọc để xác định tài liệu cần xóa.

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Bộ lọc theo ObjectId
document_to_delete = {"_id": ObjectId("62d6e04ecab6d8e130497485")}

# Tìm tài liệu trước khi xóa
print("Tìm tài liệu trước khi xóa: ")
pprint(accounts_collection.find_one(document_to_delete))

# Thực hiện xóa
result = accounts_collection.delete_one(document_to_delete)

# Tìm tài liệu sau khi xóa
print("Tìm tài liệu sau khi xóa: ")
pprint(accounts_collection.find_one(document_to_delete))

print("Tài liệu đã xóa: " + str(result.deleted_count))

# Đóng kết nối
client.close()
```

### Xóa Nhiều Tài Liệu (Delete Multiple Documents)

Để xóa nhiều tài liệu, sử dụng phương thức `delete_many()`. Phương thức này nhận một bộ lọc và xóa tất cả các tài liệu khớp.

```python
from pymongo import MongoClient
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Bộ lọc
documents_to_delete = {"balance": {"$lt": 2000}}

# Tìm tài liệu mẫu trước khi xóa
print("Tìm tài liệu mẫu trước khi xóa: ")
pprint(accounts_collection.find_one(documents_to_delete))

# Thực hiện xóa
result = accounts_collection.delete_many(documents_to_delete)

# Tìm tài liệu mẫu sau khi xóa
print("Tìm tài liệu mẫu sau khi xóa: ")
pprint(accounts_collection.find_one(documents_to_delete))

print("Tài liệu đã xóa: " + str(result.deleted_count))

# Đóng kết nối
client.close()
```

## Tạo Giao dịch Đa Tài Liệu (Creating Multi-Document Transactions)

Giao dịch đa tài liệu cho phép thực hiện nhiều thao tác như một đơn vị nguyên tử, đảm bảo tính toàn vẹn dữ liệu. Để tạo giao dịch, bạn cần định nghĩa một hàm callback chứa các thao tác và sử dụng phiên (session) để quản lý giao dịch.

### Quy trình

1. **Kết nối tới MongoDB**: Đảm bảo có kết nối hoạt động.
2. **Định nghĩa callback**: Xác định chuỗi thao tác trong giao dịch, truyền phiên (session) và các tham số cần thiết.
3. **Lấy tham chiếu collection**: Xác định các collection liên quan.
4. **Thực hiện thao tác**: Thêm các thao tác và truyền phiên vào mỗi thao tác.
5. **Bắt đầu phiên**: Sử dụng `start_session()` trong khối `with`.
6. **Thực thi giao dịch**: Gọi `with_transaction()` để bắt đầu, thực hiện callback, và xác nhận (hoặc hủy nếu có lỗi).

### Ví dụ mã

```python
from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Bước 1: Định nghĩa callback cho các thao tác trong giao dịch
def callback(
    session,
    transfer_id=None,
    account_id_receiver=None,
    account_id_sender=None,
    transfer_amount=None,
):
    # Lấy tham chiếu tới collection 'accounts'
    accounts_collection = session.client.bank.accounts

    # Lấy tham chiếu tới collection 'transfers'
    transfers_collection = session.client.bank.transfers

    # Tạo tài liệu chuyển khoản
    transfer = {
        "transfer_id": transfer_id,
        "to_account": account_id_receiver,
        "from_account": account_id_sender,
        "amount": {"$numberDecimal": str(transfer_amount)},
    }

    # Các thao tác giao dịch
    # Cập nhật tài khoản người gửi: trừ số dư và thêm ID chuyển khoản
    accounts_collection.update_one(
        {"account_id": account_id_sender},
        {
            "$inc": {"balance": -transfer_amount},
            "$push": {"transfers_complete": transfer_id},
        },
        session=session,
    )

    # Cập nhật tài khoản người nhận: cộng số dư và thêm ID chuyển khoản
    accounts_collection.update_one(
        {"account_id": account_id_receiver},
        {
            "$inc": {"balance": transfer_amount},
            "$push": {"transfers_complete": transfer_id},
        },
        session=session,
    )

    # Thêm thông tin chuyển khoản vào collection 'transfers'
    transfers_collection.insert_one(transfer, session=session)

    print("Giao dịch thành công")

    return

# Bọc callback để truyền tham số
def callback_wrapper(s):
    callback(
        s,
        transfer_id="TR218721873",
        account_id_receiver="MDB343652528",
        account_id_sender="MDB574189300",
        transfer_amount=100,
    )

# Bước 2: Bắt đầu phiên
with client.start_session() as session:
    # Bước 3: Thực thi giao dịch
    session.with_transaction(callback_wrapper)

# Đóng kết nối
client.close()
```

### Lưu ý

- **Callback**: Định nghĩa các thao tác giao dịch, luôn truyền `session` vào mỗi thao tác.
- **with_transaction**: Tự động xác nhận giao dịch nếu thành công hoặc hủy nếu có lỗi.
- **Tham số**: Sử dụng hàm bọc (wrapper) hoặc lambda để truyền các tham số bổ sung vào callback.
- **Hiệu suất**: Giữ giao dịch ngắn gọn để tránh ảnh hưởng đến hiệu suất.



---
# Hiểu về Wrapper trong Python và Giao dịch MongoDB

## Giải thích Wrapper trong Code Giao dịch MongoDB

Trong đoạn code giao dịch MongoDB sử dụng PyMongo, hàm `callback_wrapper` được sử dụng để hỗ trợ việc truyền các tham số bổ sung vào hàm `callback` khi thực hiện giao dịch bằng phương thức `with_transaction`. Hãy phân tích chi tiết cách wrapper được sử dụng trong đoạn code này:

### Đoạn code liên quan

```python
# Định nghĩa hàm callback
def callback(
    session,
    transfer_id=None,
    account_id_receiver=None,
    account_id_sender=None,
    transfer_amount=None,
):
    accounts_collection = session.client.bank.accounts
    transfers_collection = session.client.bank.transfers
    transfer = {
        "transfer_id": transfer_id,
        "to_account": account_id_receiver,
        "from_account": account_id_sender,
        "amount": {"$numberDecimal": str(transfer_amount)},
    }
    accounts_collection.update_one(
        {"account_id": account_id_sender},
        {
            "$inc": {"balance": -transfer_amount},
            "$push": {"transfers_complete": transfer_id},
        },
        session=session,
    )
    accounts_collection.update_one(
        {"account_id": account_id_receiver},
        {
            "$inc": {"balance": transfer_amount},
            "$push": {"transfers_complete": transfer_id},
        },
        session=session,
    )
    transfers_collection.insert_one(transfer, session=session)
    print("Giao dịch thành công")
    return

# Định nghĩa wrapper
def callback_wrapper(s):
    callback(
        s,
        transfer_id="TR218721873",
        account_id_receiver="MDB343652528",
        account_id_sender="MDB574189300",
        transfer_amount=100,
    )

# Thực thi giao dịch
with client.start_session() as session:
    session.with_transaction(callback_wrapper)
```

### Tại sao cần wrapper?

Phương thức `session.with_transaction()` yêu cầu một hàm callback với **chữ ký (signature)** chỉ nhận một tham số là `session`. Tuy nhiên, trong thực tế, hàm `callback` của chúng ta cần thêm các tham số khác để thực hiện giao dịch, như `transfer_id`, `account_id_receiver`, `account_id_sender`, và `transfer_amount`. Điều này tạo ra vấn đề vì:

- `with_transaction()` chỉ chấp nhận một hàm có dạng `func(session)`.
- Hàm `callback` của chúng ta có dạng `callback(session, transfer_id, account_id_receiver, account_id_sender, transfer_amount)`.

Để giải quyết vấn đề này, chúng ta tạo một hàm **wrapper** (`callback_wrapper`) với chữ ký phù hợp (`func(session)`), và bên trong wrapper, gọi hàm `callback` với đầy đủ các tham số cần thiết.

### Cách hoạt động của wrapper trong code

1. **Hàm callback**:
   - Định nghĩa các thao tác giao dịch (cập nhật tài khoản người gửi, người nhận, và thêm bản ghi chuyển khoản).
   - Nhận nhiều tham số để tùy chỉnh giao dịch cụ thể.

2. **Hàm callback_wrapper**:
   - Nhận một tham số duy nhất là `session`, phù hợp với yêu cầu của `with_transaction`.
   - Gọi hàm `callback` và truyền vào `session` cùng với các tham số cụ thể của giao dịch (ví dụ: `transfer_id="TR218721873"`).
   - Đóng vai trò như một "cầu nối" giữa `with_transaction` và `callback`.

3. **Thực thi giao dịch**:
   - `with_transaction(callback_wrapper)` gọi `callback_wrapper(session)`, sau đó `callback_wrapper` gọi `callback` với các tham số đầy đủ.
   - Điều này đảm bảo rằng giao dịch được thực hiện đúng với các giá trị mong muốn.

### Lý do sử dụng wrapper thay vì lambda

Trong tài liệu, có đề cập rằng cách tốt nhất để truyền tham số bổ sung là sử dụng **lambda**. Ví dụ, thay vì `callback_wrapper`, bạn có thể viết:

```python
with client.start_session() as session:
    session.with_transaction(
        lambda s: callback(
            s,
            transfer_id="TR218721873",
            account_id_receiver="MDB343652528",
            account_id_sender="MDB574189300",
            transfer_amount=100,
        )
    )
```

Tuy nhiên, trong đoạn code này, tác giả chọn sử dụng một hàm wrapper riêng (`callback_wrapper`) vì:

- **Đơn giản hóa cú pháp**: Đối với một số nhà phát triển, việc định nghĩa một hàm wrapper rõ ràng dễ đọc hơn so với biểu thức lambda, đặc biệt khi các tham số phức tạp hoặc cần tái sử dụng.
- **Tái sử dụng**: Nếu cần gọi giao dịch với cùng tham số ở nhiều nơi, hàm wrapper có thể được tái sử dụng dễ dàng.
- **Tính rõ ràng**: Một hàm wrapper đặt tên rõ ràng (như `callback_wrapper`) giúp mã dễ hiểu hơn về ý định.

### Hạn chế của wrapper trong trường hợp này

- **Khả năng tái sử dụng hạn chế**: Hàm `callback_wrapper` được viết cứng với các tham số cụ thể (`transfer_id="TR218721873"`, v.v.), nên chỉ phù hợp cho một giao dịch cụ thể. Nếu cần thực hiện giao dịch khác, bạn phải tạo wrapper mới hoặc sửa đổi wrapper hiện tại.
- **So với lambda**: Lambda linh hoạt hơn vì bạn có thể truyền các tham số khác nhau ngay tại nơi gọi mà không cần định nghĩa hàm mới.

---

## Giảng chi tiết về Wrapper trong Python

### Wrapper là gì?

Trong Python, một **wrapper** (hay còn gọi là decorator hoặc hàm bọc) là một hàm (hoặc một cấu trúc) được sử dụng để "bọc" một hàm khác nhằm:

- Thêm chức năng bổ sung trước hoặc sau khi hàm chính được gọi.
- Sửa đổi tham số hoặc kết quả của hàm chính.
- Điều chỉnh cách hàm chính hoạt động mà không thay đổi mã nguồn của nó.

Wrapper thường được sử dụng trong các tình huống như:

- **Ghi log**: Ghi lại thông tin khi hàm được gọi.
- **Kiểm tra quyền truy cập**: Kiểm tra xem người dùng có quyền thực thi hàm hay không.
- **Đo thời gian thực thi**: Tính toán thời gian chạy của hàm.
- **Sửa đổi tham số**: Điều chỉnh tham số trước khi truyền vào hàm chính, như trong trường hợp MongoDB ở trên.

### Cách hoạt động của Wrapper

Wrapper thường là một hàm nhận một hàm khác làm tham số, trả về một hàm mới (hàm bọc) thực hiện một số thao tác trước/sau khi gọi hàm gốc. Trong Python, điều này thường được thực hiện bằng cách sử dụng **closures** hoặc **decorators**.

#### Ví dụ cơ bản về Wrapper

```python
def my_wrapper(func):
    def inner(*args, **kwargs):
        print("Trước khi gọi hàm")
        result = func(*args, **kwargs)
        print("Sau khi gọi hàm")
        return result
    return inner

def say_hello(name):
    print(f"Xin chào, {name}!")

# Áp dụng wrapper
say_hello = my_wrapper(say_hello)
say_hello("Alice")
```

**Kết quả**:
```
Trước khi gọi hàm
Xin chào, Alice!
Sau khi gọi hàm
```

Trong ví dụ này:

- `my_wrapper` là hàm wrapper, nhận hàm `say_hello` làm tham số.
- `inner` là hàm bọc, thực hiện các thao tác trước/sau khi gọi `say_hello`.
- `say_hello` được gán lại thành hàm bọc, nên khi gọi `say_hello("Alice")`, nó thực thi logic của `inner`.

#### Sử dụng Decorator (@)

Python cung cấp cú pháp **decorator** bằng ký hiệu `@` để áp dụng wrapper một cách gọn gàng hơn:

```python
def my_wrapper(func):
    def inner(*args, **kwargs):
        print("Trước khi gọi hàm")
        result = func(*args, **kwargs)
        print("Sau khi gọi hàm")
        return result
    return inner

@my_wrapper
def say_hello(name):
    print(f"Xin chào, {name}!")

say_hello("Alice")
```

Ký hiệu `@my_wrapper` tương đương với `say_hello = my_wrapper(say_hello)`.

### Wrapper và Closure

Wrapper dựa trên khái niệm **closure** trong Python. Một closure là một hàm bên trong có thể truy cập các biến từ phạm vi bao quanh nó, ngay cả khi hàm bao quanh đã kết thúc. Trong ví dụ trên, hàm `inner` là một closure vì nó sử dụng biến `func` từ hàm `my_wrapper`.

### Wrapper trong trường hợp MongoDB

Trong đoạn code MongoDB, `callback_wrapper` không phải là một decorator theo nghĩa truyền thống, nhưng nó hoạt động như một wrapper vì:

- Nó bọc hàm `callback` để điều chỉnh cách gọi hàm (thêm các tham số cụ thể).
- Nó đảm bảo rằng `with_transaction` nhận một hàm có chữ ký phù hợp (`func(session)`).
- Nó tương tự như một hàm bọc đơn giản, gọi hàm chính (`callback`) với các tham số bổ sung.

### Các ứng dụng thực tế của Wrapper

1. **Đo thời gian thực thi**:
   ```python
   import time

   def timing_wrapper(func):
       def inner(*args, **kwargs):
           start = time.time()
           result = func(*args, **kwargs)
           end = time.time()
           print(f"{func.__name__} chạy mất {end - start} giây")
           return result
       return inner

   @timing_wrapper
   def slow_function():
       time.sleep(1)
       return "Hoàn thành"

   print(slow_function())
   ```

2. **Kiểm tra quyền truy cập**:
   ```python
   def require_login(func):
       def inner(user, *args, **kwargs):
           if user.get("is_logged_in"):
               return func(user, *args, **kwargs)
           else:
               return "Vui lòng đăng nhập"
       return inner

   @require_login
   def view_profile(user):
       return f"Chào {user['name']}"

   user = {"name": "Alice", "is_logged_in": False}
   print(view_profile(user))  # In: Vui lòng đăng nhập
   ```

3. **Xử lý ngoại lệ**:
   ```python
   def handle_exceptions(func):
       def inner(*args, **kwargs):
           try:
               return func(*args, **kwargs)
           except Exception as e:
               print(f"Lỗi: {e}")
               return None
       return inner

   @handle_exceptions
   def divide(a, b):
       return a / b

   print(divide(10, 0))  # In: Lỗi: division by zero, trả về None
   ```

### So sánh Wrapper và Lambda

Trong trường hợp MongoDB, bạn có thể thay `callback_wrapper` bằng một lambda để đạt được kết quả tương tự:

```python
with client.start_session() as session:
    session.with_transaction(
        lambda s: callback(
            s,
            transfer_id="TR218721873",
            account_id_receiver="MDB343652528",
            account_id_sender="MDB574189300",
            transfer_amount=100,
        )
    )
```

- **Ưu điểm của lambda**:
  - Gọn gàng, không cần định nghĩa hàm riêng.
  - Linh hoạt, dễ thay đổi tham số ngay tại nơi gọi.
- **Nhược điểm của lambda**:
  - Có thể khó đọc nếu logic phức tạp.
  - Không tái sử dụng được như một hàm wrapper riêng.

- **Ưu điểm của wrapper**:
  - Rõ ràng, dễ hiểu về ý định.
  - Có thể tái sử dụng nếu được thiết kế tổng quát hơn.
- **Nhược điểm của wrapper**:
  - Cần định nghĩa hàm bổ sung, làm mã dài hơn.
  - Thiếu linh hoạt nếu viết cứng tham số như trong ví dụ MongoDB.

### Thực hành tốt nhất khi sử dụng Wrapper

1. **Sử dụng `@wraps` để bảo toàn thông tin hàm gốc**:
   Khi viết decorator, sử dụng `functools.wraps` để bảo toàn tên, tài liệu, và các thuộc tính khác của hàm gốc:

   ```python
   from functools import wraps

   def my_wrapper(func):
       @wraps(func)
       def inner(*args, **kwargs):
           print("Trước khi gọi hàm")
           result = func(*args, **kwargs)
           print("Sau khi gọi hàm")
           return result
       return inner

   @my_wrapper
   def say_hello(name):
       """In lời chào"""
       print(f"Xin chào, {name}!")

   print(say_hello.__name__)  # In: say_hello
   print(say_hello.__doc__)   # In: In lời chào
   ```

   Nếu không dùng `@wraps`, `say_hello.__name__` sẽ trả về `inner`, gây khó khăn khi debug.

2. **Giữ wrapper đơn giản**:
   Chỉ thêm logic cần thiết để tránh làm hàm chính phức tạp hơn.

3. **Sử dụng khi cần tái sử dụng**:
   Nếu logic wrapper được dùng ở nhiều nơi, định nghĩa một hàm wrapper riêng thay vì lặp lại lambda.

4. **Kiểm tra lỗi**:
   Đảm bảo wrapper xử lý lỗi một cách phù hợp, đặc biệt trong các trường hợp như giao dịch MongoDB.

### Kết luận

Trong đoạn code MongoDB, `callback_wrapper` là một wrapper đơn giản giúp điều chỉnh chữ ký của hàm `callback` để phù hợp với yêu cầu của `with_transaction`. Nó đóng vai trò như một cầu nối, cho phép truyền các tham số bổ sung mà không làm thay đổi hàm chính. Trong Python nói chung, wrapper là một công cụ mạnh mẽ để mở rộng chức năng của hàm, thường được sử dụng thông qua closures hoặc decorators. Hiểu cách sử dụng wrapper và các lựa chọn thay thế như lambda giúp bạn viết mã linh hoạt, dễ bảo trì, và phù hợp với các tình huống thực tế như giao dịch cơ sở dữ liệu.

# Sử dụng Aggregation Stages trong MongoDB với Python

Phần này hướng dẫn cách sử dụng các giai đoạn **aggregation** (`$match`, `$group`, `$sort`, `$project`) trong MongoDB bằng thư viện **PyMongo** để xử lý và biến đổi dữ liệu.

## Sử dụng `$match` và `$group`

### Giai đoạn `$match`

- **Mục đích**: Lọc các tài liệu dựa trên điều kiện truy vấn, chỉ truyền các tài liệu khớp sang giai đoạn tiếp theo.
- **Vị trí**: Nên đặt sớm trong pipeline để giảm số lượng tài liệu cần xử lý ở các giai đoạn sau.
- **Cú pháp**: Nhận một tài liệu xác định điều kiện truy vấn.

**Ví dụ**:

```python
# Lọc các tài khoản có số dư dưới 1000
select_by_balance = {"$match": {"balance": {"$lt": 1000}}}
```

### Giai đoạn `$group`

- **Mục đích**: Nhóm các tài liệu theo một khóa nhóm (group key) và tính toán các giá trị tổng hợp (ví dụ: trung bình, tổng, đếm).
- **Yêu cầu**: Phải có trường `_id` xác định khóa nhóm, sử dụng `$` để tham chiếu trường.
- **Cú pháp**: Có thể bao gồm các trường tính toán bằng các toán tử tích lũy như `$avg`, `$sum`, `$count`.

**Ví dụ**:

```python
# Nhóm tài liệu theo loại tài khoản và tính số dư trung bình
separate_by_account_calculate_avg_balance = {
    "$group": {"_id": "$account_type", "avg_balance": {"$avg": "$balance"}}
}
```

### Ví dụ Aggregation Pipeline với `$match` và `$group`

Pipeline dưới đây lọc các tài khoản có số dư dưới 1000, sau đó nhóm theo loại tài khoản và tính số dư trung bình.

```python
from pymongo import MongoClient
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Lọc các tài khoản có số dư dưới 1000
select_by_balance = {"$match": {"balance": {"$lt": 1000}}}

# Nhóm theo loại tài khoản và tính số dư trung bình
separate_by_account_calculate_avg_balance = {
    "$group": {"_id": "$account_type", "avg_balance": {"$avg": "$balance"}}
}

# Tạo pipeline
pipeline = [
    select_by_balance,
    separate_by_account_calculate_avg_balance,
]

# Thực hiện aggregation
results = accounts_collection.aggregate(pipeline)

# In kết quả
print()
print("Số dư trung bình của các tài khoản checking và savings có số dư dưới 1000:", "\n")
for item in results:
    pprint(item)

# Đóng kết nối
client.close()
```

## Sử dụng `$sort` và `$project`

### Giai đoạn `$sort`

- **Mục đích**: Sắp xếp các tài liệu theo thứ tự tăng dần hoặc giảm dần dựa trên một hoặc nhiều trường.
- **Cú pháp**: Nhận một tài liệu xác định trường cần sắp xếp và thứ tự (`1` cho tăng dần, `-1` cho giảm dần).

**Ví dụ**:

```python
# Sắp xếp tài liệu theo số dư từ cao đến thấp
organize_by_original_balance = {"$sort": {"balance": -1}}
```

### Giai đoạn `$project`

- **Mục đích**: Chỉ định các trường trả về trong kết quả, có thể bao gồm, loại trừ, hoặc tạo trường mới.
- **Cách dùng**:
  - Đặt trường là `1` để bao gồm, `0` để loại trừ.
  - Tạo trường mới bằng cách sử dụng biểu thức, ví dụ: tính toán giá trị mới từ các trường hiện có.
- **Vị trí**: Thường đặt ở cuối pipeline để định dạng kết quả cuối cùng.

**Ví dụ**:

```python
# Trả về loại tài khoản, số dư, và số dư quy đổi sang GBP, loại bỏ _id
return_specified_fields = {
    "$project": {
        "account_type": 1,
        "balance": 1,
        "gbp_balance": {"$divide": ["$balance", conversion_rate_usd_to_gbp]},
        "_id": 0,
    }
}
```

### Ví dụ Aggregation Pipeline với `$match`, `$sort`, và `$project`

Pipeline dưới đây lọc các tài khoản checking có số dư trên 1500, sắp xếp theo số dư giảm dần, và trả về loại tài khoản, số dư gốc, cùng số dư quy đổi sang GBP.

```python
from pymongo import MongoClient
from pprint import pprint

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017")

# Lấy tham chiếu tới database 'bank'
db = client.bank

# Lấy tham chiếu tới collection 'accounts'
accounts_collection = db.accounts

# Tỷ giá quy đổi USD sang GBP
conversion_rate_usd_to_gbp = 1.3

# Lọc các tài khoản checking có số dư trên 1500
select_accounts = {"$match": {"account_type": "checking", "balance": {"$gt": 1500}}}

# Sắp xếp theo số dư từ cao đến thấp
organize_by_original_balance = {"$sort": {"balance": -1}}

# Trả về loại tài khoản, số dư, và số dư quy đổi sang GBP
return_specified_fields = {
    "$project": {
        "account_type": 1,
        "balance": 1,
        "gbp_balance": {"$divide": ["$balance", conversion_rate_usd_to_gbp]},
        "_id": 0,
    }
}

# Tạo pipeline
pipeline = [
    select_accounts,
    organize_by_original_balance,
    return_specified_fields,
]

# Thực hiện aggregation
results = accounts_collection.aggregate(pipeline)

# In kết quả
print(
    "Loại tài khoản, số dư gốc và số dư quy đổi sang GBP của các tài khoản checking có số dư trên 1500, "
    "sắp xếp từ cao đến thấp:", "\n"
)
for item in results:
    pprint(item)

# Đóng kết nối
client.close()
```

## Lưu ý khi sử dụng Aggregation Pipeline

- **Tối ưu hóa pipeline**: Đặt `$match` sớm để giảm số lượng tài liệu xử lý, và `$project` ở cuối để định dạng kết quả.
- **Hiệu suất**: Aggregation trên tập dữ liệu lớn có thể tốn tài nguyên, hãy đảm bảo sử dụng index phù hợp.
- **Kiểm tra kết quả**: Sử dụng `pprint` hoặc các công cụ trực quan hóa để kiểm tra dữ liệu trả về.