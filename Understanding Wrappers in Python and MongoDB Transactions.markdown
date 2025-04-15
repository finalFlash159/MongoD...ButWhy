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